import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, ClockCycles
import random

# --- Test Configuration ---
CLOCK_PERIOD_NS = 10  # 100 MHz clock
PWM_PERIOD_CYCLES = 4096 # For a 12-bit DAC, one full PWM cycle is 2^12 clock cycles

async def reset_dut(dut):
    """Resets the DUT."""
    dut._log.info("Resetting DUT")
    dut.rst_n.value = 0
    # The DAC input pins
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 5)
    dut._log.info("Reset complete")

async def run_dac_test(dut, dac_value):
    """Sets a DAC value and verifies the PWM output duty cycle."""
    dut._log.info(f"Testing DAC value: {dac_value}")

    # Set the 12-bit input value on the DUT pins
    # ui_in holds the upper 8 bits [11:4]
    # uio_in holds the lower 4 bits [3:0]
    dut.ui_in.value = (dac_value >> 4) & 0xFF
    dut.uio_in.value = dac_value & 0x0F

    # Wait for the new value to propagate and for a full PWM cycle to start
    await ClockCycles(dut.clk, 10)

    # Measure the number of high cycles over one full PWM period
    high_cycles_count = 0
    for _ in range(PWM_PERIOD_CYCLES):
        await RisingEdge(dut.clk)
        if dut.uo_out[0].value == 1:
            high_cycles_count += 1

    dut._log.info(f"Input: {dac_value}, Measured high cycles: {high_cycles_count}")

    # The number of high cycles should be exactly equal to the input value
    assert high_cycles_count == dac_value, f"Failed for input {dac_value}: expected {dac_value} high cycles, but got {high_cycles_count}"

@cocotb.test()
async def test_dac_functionality(dut):
    """Test the 12-bit PWM DAC with various input values."""
    # Start the clock
    clock = Clock(dut.clk, CLOCK_PERIOD_NS, units="ns")
    cocotb.start_soon(clock.start())

    # Perform reset
    await reset_dut(dut)

    # --- Run a series of tests ---
    # Test zero
    await run_dac_test(dut, 0)

    # Test a small value
    await run_dac_test(dut, 100)

    # Test quarter-scale value
    await run_dac_test(dut, 1024)

    # Test half-scale value
    await run_dac_test(dut, 2048)

    # Test a high value
    await run_dac_test(dut, 3500)

    # Test maximum value
    await run_dac_test(dut, 4095)

    dut._log.info("All DAC tests passed successfully!")
