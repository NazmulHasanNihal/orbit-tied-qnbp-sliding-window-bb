// =============================================================================
// File: rtl/g3_gate.sv
// Module: g3_gate (Fast-Path Confidence Margin Gate G3)
// Project: Orbit-Tied Quantized Neural Belief Propagation (QNBP)
// Description: Hardware evaluator for the G3 margin-gated fast path. Checks both
//              exact syndrome convergence and minimum LLR margin confidence:
//              Accept <=> (SyndromeValid) AND (min_v |L_v| >= tau_int).
// Standard: IEEE 1800-2017 SystemVerilog
// Synthesis Target: Xilinx UltraScale+ / AMD Versal (Zero DSP Slices: DSP = 0)
// =============================================================================

`timescale 1ns / 1ps

module g3_gate #(
    parameter int WIDTH     = 6,         // Quantization bit-width
    parameter int NUM_NODES = 72,        // Number of committed variable nodes
    parameter int MAG_W     = WIDTH - 1  // Magnitude bit-width
) (
    input  logic                               clk,
    input  logic                               rst_n,
    input  logic                               enable,

    // Tentative posterior LLRs from VNU array
    input  logic signed [WIDTH-1:0]            posterior_llrs [NUM_NODES],

    // Parity-check syndrome satisfaction flag (all checks satisfied)
    input  logic                               syndrome_valid,

    // Integer confidence margin threshold: tau_int = round(tau / Delta)
    input  logic [MAG_W-1:0]                   tau_threshold,

    // Fast-path decision output
    output logic                               gate_accept,
    output logic [MAG_W-1:0]                   min_margin
);

    logic [MAG_W-1:0] node_mags [NUM_NODES];
    logic [MAG_W-1:0] current_min;

    // 1. Extract absolute values of posterior LLRs
    always_comb begin
        for (int i = 0; i < NUM_NODES; i++) begin
            if (posterior_llrs[i][WIDTH-1]) begin
                if (posterior_llrs[i] == {1'b1, {(WIDTH-1){1'b0}}}) begin
                    node_mags[i] = {MAG_W{1'b1}};
                end else begin
                    node_mags[i] = -posterior_llrs[i];
                end
            end else begin
                node_mags[i] = posterior_llrs[i][MAG_W-1:0];
            end
        end
    end

    // 2. Balanced minimum reduction tree across all nodes
    always_comb begin
        current_min = {MAG_W{1'b1}};
        for (int i = 0; i < NUM_NODES; i++) begin
            if (node_mags[i] < current_min) begin
                current_min = node_mags[i];
            end
        end
    end

    // 3. Register gate decision
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            gate_accept <= 1'b0;
            min_margin  <= '0;
        end else if (enable) begin
            min_margin <= current_min;
            if (syndrome_valid && (current_min >= tau_threshold)) begin
                gate_accept <= 1'b1; // Fast-path acceptance: commit without OSD
            end else begin
                gate_accept <= 1'b0; // Reject: dispatch window to slow OSD queue
            end
        end
    end

endmodule
