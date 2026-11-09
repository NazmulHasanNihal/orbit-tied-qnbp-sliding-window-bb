// =============================================================================
// File: rtl/vnu.sv
// Module: vnu (Variable Node Unit)
// Project: Orbit-Tied Quantized Neural Belief Propagation (QNBP)
// Description: Multiplier-free Variable Node Unit executing fixed-point LLR updates
//              with canonical signed-digit (CSD) shift-and-add arithmetic.
// Standard: IEEE 1800-2017 SystemVerilog
// Synthesis Target: Xilinx UltraScale+ / AMD Versal (Zero DSP Slices: DSP = 0)
// =============================================================================

`timescale 1ns / 1ps

module vnu #(
    parameter int WIDTH  = 6,       // Quantization bit-width (signed 2's complement)
    parameter int DEG_V  = 6,       // Variable node check degree d_v
    parameter int MAX_VAL = (1 << (WIDTH - 1)) - 1, // Saturation bound (+31 for 6-bit)
    parameter int MIN_VAL = -MAX_VAL                // Symmetric bound (-31 for 6-bit)
) (
    input  logic                               clk,
    input  logic                               rst_n,
    input  logic                               enable,
    
    // Channel prior LLR: L_v^(0)
    input  logic signed [WIDTH-1:0]            prior_llr,
    
    // Extrinsic check-to-variable incoming messages: L_{c -> v}
    input  logic signed [WIDTH-1:0]            c2v_messages [DEG_V],
    
    // Previous iteration self-message for memory damping: L_{v -> c}^(t-1)
    input  logic signed [WIDTH-1:0]            prev_v2c     [DEG_V],
    
    // Damping configuration: gamma = 0.75 -> L - (L >>> 2)
    input  logic                               enable_damping,
    
    // Total a posteriori LLR output: L_v^(t)
    output logic signed [WIDTH-1:0]            posterior_llr,
    
    // Extrinsic variable-to-check outgoing messages: L_{v -> c}^(t)
    output logic signed [WIDTH-1:0]            v2c_messages [DEG_V]
);

    // Intermediate accumulation word width to prevent internal overflow
    localparam int ACC_WIDTH = WIDTH + $clog2(DEG_V + 2);
    
    logic signed [ACC_WIDTH-1:0] sum_all_checks;
    logic signed [ACC_WIDTH-1:0] total_accum;
    logic signed [ACC_WIDTH-1:0] v2c_raw [DEG_V];

    // 1. Accumulate all incoming check-to-variable messages
    always_comb begin
        sum_all_checks = '0;
        for (int i = 0; i < DEG_V; i++) begin
            sum_all_checks += c2v_messages[i];
        end
        total_accum = prior_llr + sum_all_checks;
    end

    // 2. Symmetric saturation function
    function automatic logic signed [WIDTH-1:0] saturate(input logic signed [ACC_WIDTH-1:0] val);
        if (val > MAX_VAL) begin
            return MAX_VAL[WIDTH-1:0];
        end else if (val < MIN_VAL) begin
            return MIN_VAL[WIDTH-1:0];
        end else begin
            return val[WIDTH-1:0];
        end
    endfunction

    // 3. Multiplier-free memory damping using arithmetic right shifts
    //    gamma = 0.75 = 1 - 2^(-2) => L - (L >>> 2)
    function automatic logic signed [WIDTH-1:0] apply_damping(input logic signed [WIDTH-1:0] val);
        logic signed [WIDTH-1:0] shifted;
        shifted = val >>> 2;
        return val - shifted;
    endfunction

    // 4. Output register updates (Single-cycle pipelined stage)
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            posterior_llr <= '0;
            for (int i = 0; i < DEG_V; i++) begin
                v2c_messages[i] <= '0;
            end
        end else if (enable) begin
            posterior_llr <= saturate(total_accum);

            for (int i = 0; i < DEG_V; i++) begin
                logic signed [ACC_WIDTH-1:0] damped_term;
                if (enable_damping) begin
                    damped_term = apply_damping(prev_v2c[i]);
                end else begin
                    damped_term = '0;
                end
                
                // Extrinsic message: total sum minus incident check minus memory damping
                v2c_raw[i] = total_accum - c2v_messages[i] - damped_term;
                v2c_messages[i] <= saturate(v2c_raw[i]);
            end
        end
    end

endmodule
