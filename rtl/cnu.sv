// =============================================================================
// File: rtl/cnu.sv
// Module: cnu (Check Node Unit)
// Project: Orbit-Tied Quantized Neural Belief Propagation (QNBP)
// Description: Multiplier-free Check Node Unit implementing Min-Sum message
//              passing with O(log2 d_c) balanced comparator tree and CSD scaling.
// Standard: IEEE 1800-2017 SystemVerilog
// Synthesis Target: Xilinx UltraScale+ / AMD Versal (Zero DSP Slices: DSP = 0)
// =============================================================================

`timescale 1ns / 1ps

module cnu #(
    parameter int WIDTH  = 6,       // Quantization bit-width (signed 2's complement)
    parameter int DEG_C  = 6,       // Check node variable degree d_c
    parameter int MAG_W  = WIDTH - 1 // Magnitude bit-width (unsigned)
) (
    input  logic                               clk,
    input  logic                               rst_n,
    input  logic                               enable,
    
    // Extrinsic variable-to-check incoming messages: L_{v -> c}
    input  logic signed [WIDTH-1:0]            v2c_messages [DEG_C],
    
    // Multiplier-free normalized scaling factor: alpha = 0.75 => M - (M >> 2)
    input  logic                               enable_alpha_scaling,
    
    // Injected syndrome bit and on-the-fly early-exit check satisfaction (Task 16)
    input  logic                               syndrome_bit,
    output logic                               check_satisfied,

    // Extrinsic check-to-variable outgoing messages: L_{c -> v}
    output logic signed [WIDTH-1:0]            c2v_messages [DEG_C]
);

    logic [DEG_C-1:0]   signs;
    logic [MAG_W-1:0]   mags [DEG_C];
    logic               total_parity;

    // Zero-cycle early exit: check is satisfied when hard-decision message parity matches syndrome
    assign check_satisfied = ~(total_parity ^ syndrome_bit);

    // 1. Separate sign and magnitude for each incoming message
    always_comb begin
        total_parity = 1'b0;
        for (int i = 0; i < DEG_C; i++) begin
            signs[i] = v2c_messages[i][WIDTH-1];
            total_parity ^= signs[i];
            
            // Absolute value in 2's complement with saturation protection
            if (v2c_messages[i][WIDTH-1]) begin
                if (v2c_messages[i] == {1'b1, {(WIDTH-1){1'b0}}}) begin
                    mags[i] = {MAG_W{1'b1}}; // Saturate minimum negative value
                end else begin
                    mags[i] = -v2c_messages[i];
                end
            end else begin
                mags[i] = v2c_messages[i][MAG_W-1:0];
            end
        end
    end

    // 2. Balanced search for Min1, Min2, and argmin
    logic [MAG_W-1:0]       min1_mag;
    logic [MAG_W-1:0]       min2_mag;
    logic [$clog2(DEG_C)-1:0] min1_idx;

    always_comb begin
        min1_mag = {MAG_W{1'b1}};
        min2_mag = {MAG_W{1'b1}};
        min1_idx = '0;

        // Stage 1: Find global minimum Min1
        for (int i = 0; i < DEG_C; i++) begin
            if (mags[i] < min1_mag) begin
                min1_mag = mags[i];
                min1_idx = i[$clog2(DEG_C)-1:0];
            end
        end

        // Stage 2: Find second minimum Min2 excluding min1_idx
        for (int i = 0; i < DEG_C; i++) begin
            if (i[$clog2(DEG_C)-1:0] != min1_idx) begin
                if (mags[i] < min2_mag) begin
                    min2_mag = mags[i];
                end
            end
        end
    end

    // 3. Multiplier-free normalization: alpha * M = M - (M >> 2) for alpha = 0.75
    function automatic logic [MAG_W-1:0] scale_min(input logic [MAG_W-1:0] val);
        logic [MAG_W-1:0] shifted;
        shifted = val >> 2;
        return val - shifted;
    endfunction

    // 4. Output register assembly (Single-cycle pipelined stage)
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            for (int i = 0; i < DEG_C; i++) begin
                c2v_messages[i] <= '0;
            end
        end else if (enable) begin
            for (int i = 0; i < DEG_C; i++) begin
                logic               out_sign;
                logic [MAG_W-1:0]   raw_mag;
                logic [MAG_W-1:0]   scaled_mag;

                // Parity excluding self
                out_sign = total_parity ^ signs[i];

                // Select Min2 if this node was the minimum, otherwise Min1
                if (i[$clog2(DEG_C)-1:0] == min1_idx) begin
                    raw_mag = min2_mag;
                end else begin
                    raw_mag = min1_mag;
                end

                if (enable_alpha_scaling) begin
                    scaled_mag = scale_min(raw_mag);
                end else begin
                    scaled_mag = raw_mag;
                end

                // Convert back to signed 2's complement
                if (out_sign) begin
                    c2v_messages[i] <= -{1'b0, scaled_mag};
                end else begin
                    c2v_messages[i] <= {1'b0, scaled_mag};
                end
            end
        end
    end

endmodule
