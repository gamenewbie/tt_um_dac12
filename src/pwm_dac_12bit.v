`default_nettype none
`timescale 1ns/1ps

module pwm_dac_12bit (
    input wire clk,
    input wire rst_n,
    input wire [11:0] dac_in,  // Your 12-bit digital input
    output wire pwm_out      // The 1-bit PWM output
);

    // A free-running 12-bit counter that increments on each clock cycle.
    reg [11:0] counter = 0;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            counter <= 12'd0;
        end else begin
            counter <= counter + 1;
        end
    end

    // The core PWM logic:
    // The output is high as long as the counter's value is less than the input value.
    // A larger dac_in value means the output stays high for more of the counter's cycle.
    assign pwm_out = (counter < dac_in);

endmodule
