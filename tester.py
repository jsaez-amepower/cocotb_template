import cocotb
from cocotb.triggers import RisingEdge
from cocotb.clock import Clock
import random
from math import floor

#this function converts an unsigned number to a signed number
def unsigned_to_signed(unsigned, bit_width):
    max_value = 2**(bit_width - 1)
    if unsigned >= max_value:
        return -1* (2**bit_width - unsigned)
    else:
        return unsigned

@cocotb.test()
async def init_testbench(dut):
    # Initialize clock
    cocotb.start_soon(Clock(dut.clk, 1, units="ns").start())

    dut.sample.value = 0
    dut.ENA.value = 0
    dut.rst_n.value = 0
    for _ in range(10):
        await RisingEdge(dut.clk)
    dut.rst_n.value = 1

    #read the parameters from the top module that were passed as arguments in the makefile
    DW = int(cocotb.top.DW)
    log2_samples = int(cocotb.top.log2_samples)
    US = int(cocotb.top.US)

    #print the parameters
    print(f"DW {DW}, log2_samples {log2_samples}, US {US}")
    
    accumulator = 0
    avg = 0
    
   
    for j in range(3):
        for i in range(10000):
            
            if US == 1:
                sample = random.randint(0, pow(2,DW) -1)  
            else:
                if j%3 == 0:  #test positive and negative values
                    sample = random.randint(-1*pow(2, DW - 1),pow(2, DW - 1) - 1)
                elif j%3 == 1: #test positive values
                    sample = random.randint(0,pow(2, DW -1) )
                elif j%3 == 2: #test negative values
                    sample = random.randint(-1*pow(2, DW - 1),0)        
             
            dut.sample.value = sample
            
            accumulator = floor(accumulator + sample - avg)
            avg = floor(accumulator/(2**log2_samples))
            expected_result = avg if US else unsigned_to_signed(avg, DW)        
            
            dut.ENA.value = 1
            await RisingEdge(dut.clk)
            dut.ENA.value = 0
            await RisingEdge(dut.clk)
            await RisingEdge(dut.clk)

            # Check the result
            result = dut.avg.value.integer if US else unsigned_to_signed(dut.avg.value.integer, DW)
            #print(f"j {j}, i {i}, Sample {sample}, Expected {expected_result}, got {result}, Accumulator {accumulator}")
            assert result == expected_result, f"j {j}, i {i}, Sample {sample}, Expected {expected_result}, got {result}, Accumulator {accumulator}"
            
        dut.sample.value = 0
        dut.rst_n.value = 0
        accumulator = 0
        avg = 0
        await RisingEdge(dut.clk)
        dut.rst_n.value = 1
        await RisingEdge(dut.clk)
    
