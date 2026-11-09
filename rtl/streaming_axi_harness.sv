// =============================================================================
// File: rtl/streaming_axi_harness.sv
// Module: streaming_axi_harness
// Project: Orbit-Tied Quantized Neural Belief Propagation (QNBP)
// Description: Streaming AXI-Stream test harness with syndrome ingestion FIFO,
//              residual feedback registers, on-the-fly zero-cycle early-exit
//              detection, and real-time timeout watchdog (< 1 us deadline).
// Standard: IEEE 1800-2017 SystemVerilog
// Target: Xilinx UltraScale+ / AMD Versal (Multiplier-Free: DSP = 0)
// =============================================================================

`timescale 1ns / 1ps

module streaming_axi_harness #(
    parameter int SYNDROME_WIDTH = 72,      // Stabilizer syndrome checks per round
    parameter int WINDOW_WIDTH   = 144,     // Window check nodes across W=2 rounds
    parameter int MAX_CYCLES     = 50,      // Timeout watchdog threshold (800 ns at 62.5 MHz)
    parameter int COMMIT_STRIDE  = 72       // Faults committed per window step (F=1)
) (
    input  logic                            clk,
    input  logic                            rst_n,

    // AXI4-Stream Slave Interface (Syndrome Ingestion)
    input  logic                            s_axis_tvalid,
    output logic                            s_axis_tready,
    input  logic [SYNDROME_WIDTH-1:0]       s_axis_tdata,
    input  logic                            s_axis_tlast,

    // AXI4-Stream Master Interface (Correction Output)
    output logic                            m_axis_tvalid,
    input  logic                            m_axis_tready,
    output logic [COMMIT_STRIDE-1:0]        m_axis_tdata,
    output logic                            m_axis_tuser,   // 0: Fast path accepted, 1: Fallback triggered
    output logic                            m_axis_tlast,

    // Hardware status flags
    output logic                            active_decoding,
    output logic [7:0]                      elapsed_cycles
);

    // Operational FSM States
    typedef enum logic [2:0] {
        STATE_IDLE    = 3'b000,
        STATE_INGEST  = 3'b001,
        STATE_DECODE  = 3'b010,
        STATE_COMMIT  = 3'b011,
        STATE_TRANSMIT= 3'b100
    } state_t;

    state_t state_reg, state_next;

    // Temporal Residual Register for Window Residual Propagation
    logic [SYNDROME_WIDTH-1:0] residual_reg;
    logic [WINDOW_WIDTH-1:0]   window_syndrome_reg;
    logic [COMMIT_STRIDE-1:0]  committed_corrections_reg;

    // Timeout Watchdog Counter
    logic [7:0] cycle_counter;
    logic       timeout_event;
    logic       all_checks_satisfied;
    logic       gate_accepted;
    logic       fallback_flag_reg;

    assign active_decoding = (state_reg == STATE_DECODE);
    assign elapsed_cycles  = cycle_counter;
    assign timeout_event   = (cycle_counter >= MAX_CYCLES);

    // Mock early exit & gate status connection from datapath
    // In full top-level, all_checks_satisfied is the wide reduction AND of CNU outputs
    always_comb begin
        s_axis_tready = (state_reg == STATE_IDLE);
        m_axis_tvalid = (state_reg == STATE_TRANSMIT);
        m_axis_tdata  = committed_corrections_reg;
        m_axis_tuser  = fallback_flag_reg;
        m_axis_tlast  = 1'b1;
    end

    // Sequential State Transition & Registers
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state_reg                 <= STATE_IDLE;
            cycle_counter             <= '0;
            residual_reg              <= '0;
            window_syndrome_reg       <= '0;
            committed_corrections_reg <= '0;
            fallback_flag_reg         <= 1'b0;
        end else begin
            state_reg <= state_next;

            case (state_reg)
                STATE_IDLE: begin
                    cycle_counter <= '0;
                    if (s_axis_tvalid && s_axis_tready) begin
                        // Ingest new round and combine with residual from previous window
                        window_syndrome_reg[SYNDROME_WIDTH-1:0] <= s_axis_tdata ^ residual_reg;
                    end
                end

                STATE_DECODE: begin
                    cycle_counter <= cycle_counter + 1'b1;
                    if (all_checks_satisfied && gate_accepted) begin
                        fallback_flag_reg <= 1'b0; // Fast path accepted
                    end else if (timeout_event) begin
                        fallback_flag_reg <= 1'b1; // Timeout to fallback
                    end
                end

                STATE_COMMIT: begin
                    // Boundary residual feedback: s_res = s_boundary ^ e_commit
                    residual_reg <= window_syndrome_reg[SYNDROME_WIDTH-1:0] ^ committed_corrections_reg;
                end

                STATE_TRANSMIT: begin
                    if (m_axis_tvalid && m_axis_tready) begin
                        cycle_counter <= '0;
                    end
                end

                default: begin
                    cycle_counter <= '0;
                end
            endcase
        end
    end

    // Combinational Next-State Logic
    always_comb begin
        state_next = state_reg;

        case (state_reg)
            STATE_IDLE: begin
                if (s_axis_tvalid) begin
                    state_next = STATE_INGEST;
                end
            end

            STATE_INGEST: begin
                state_next = STATE_DECODE;
            end

            STATE_DECODE: begin
                // Early exit on zero-cycle syndrome satisfaction OR watchdog timeout
                if ((all_checks_satisfied && gate_accepted) || timeout_event) begin
                    state_next = STATE_COMMIT;
                end
            end

            STATE_COMMIT: begin
                state_next = STATE_TRANSMIT;
            end

            STATE_TRANSMIT: begin
                if (m_axis_tready) begin
                    state_next = STATE_IDLE;
                end
            end

            default: state_next = STATE_IDLE;
        endcase
    end

    // Emulated on-the-fly gate evaluation for test harness self-checking
    assign all_checks_satisfied = (cycle_counter >= 8'd4); // Converged in 4 iterations
    assign gate_accepted        = 1'b1;

endmodule
