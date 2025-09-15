/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_dac12 (
    input  wire [7:0] ui_in,   // Dedicated inputs [11:4]
    output wire [7:0] uo_out,  // Dedicated outputs
    input  wire [7:0] uio_in,  // IOs: Input path [3:0]
    output wire [7:0] uio_out, // IOs: Output path
    output wire [7:0] uio_oe,  // IOs: Enable path
    input  wire       ena,
    input  wire       clk,
    input  wire       rst_n
);

    // --- 12-Bit DAC Implementation ---

    // 1. Combine inputs to form a 12-bit data word.
    //    Using ui_in for the most significant 8 bits and uio_in for the least significant 4 bits.
    wire [11:0] dac_input = {ui_in, uio_in[3:0]};

    // 2. This wire will carry the 1-bit PWM signal from our DAC module.
    wire pwm_signal;

    // 3. Instantiate the 12-bit PWM DAC module.
    pwm_dac_12bit my_pwm_dac (
        .clk(clk),
        .rst_n(rst_n),
        .dac_in(dac_input),
        .pwm_out(pwm_signal)
    );

    // --- Pin Assignments ---

    // 4. Route the PWM signal to a digital output pin.
    assign uo_out[0] = pwm_signal;

    // Tie off all other unused digital outputs to ground.
    assign uo_out[7:1] = 7'b0;
    assign uio_out     = 8'b0;

    // 5. Configure the bidirectional IO pins.
    //    Set uio_oe[3:0] to 0 to use them as inputs.
    //    The rest are also inputs.
    assign uio_oe = 8'b00000000; // All uio pins are inputs

endmodule
