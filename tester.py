import cocotb
from cocotb.triggers import RisingEdge
from cocotb.clock import Clock
import random

#this function converts an unsigned number to a signed number
def unsigned_to_signed(unsigned, bit_width):
    max_value = 2**(bit_width - 1)
    if unsigned >= max_value:
        return unsigned - 2**bit_width
    else:
        return unsigned

@cocotb.test()
async def init_testbench(dut):
    # Initialize clock
    cocotb.start_soon(Clock(dut.clk, 1, units="ns").start())

    dut.dataa.value = 0
    dut.datab.value = 0
    dut.clken.value = 1
    dut.nreset.value = 0
    for _ in range(10):
        await RisingEdge(dut.clk)
    dut.nreset.value = 1

    #read the parameters from the top module that were passed as arguments in the makefile
    widtha = int(cocotb.top.widtha)
    widthb = int(cocotb.top.widthb)
    widthp = int(cocotb.top.widthp)
    pipeline = int(cocotb.top.pipeline)
    us = int(cocotb.top.us)

    #print the parameters
    print(f"widtha {widtha}, widthb {widthb}, widthp {widthp}, pipeline {pipeline}, us {us}")

    for _ in range(100):
        #assign dataa and datab random values based on parameters
        if us == 1:
            a = random.randint(0,pow(2, widtha) - 1)
            b = random.randint(0,pow(2, widthb) - 1)
        else:
            a = random.randint(-1*pow(2, widtha - 1),pow(2, widtha - 1) - 1)
            b = random.randint(-1*pow(2, widthb - 1),pow(2, widthb - 1) - 1)

        dut.dataa.value = a
        dut.datab.value = b
        expected_result = a * b
        expected_result = expected_result if us else unsigned_to_signed(expected_result, widthp)
        
        # Wait for pipeline delay
        for _ in range(pipeline+1):
            await RisingEdge(dut.clk)

        # Check the result
        result = dut.result.value.integer if us else unsigned_to_signed(dut.result.value.integer, widthp)

        #print(f"A {a}, B {b}, Expected {expected_result}, got {result}")
        assert result == expected_result, f"A {a}, B {b}, Expected {expected_result}, got {result}"
