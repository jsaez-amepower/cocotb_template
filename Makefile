# Makefile

SIM ?= icarus
TOPLEVEL_LANG ?= verilog

DW ?= 32
log2_samples ?= 8
US ?= 1

VERILOG_SOURCES = MovingAvg.v
# use VHDL_SOURCES for VHDL files

# TOPLEVEL is the name of the toplevel module in your Verilog or VHDL file
TOPLEVEL = MovingAvg

# MODULE is the basename of the Python test file
MODULE = tester

# Output to file
SIM_ARGS=-l$(TOPLEVEL)_stdout.log

# Parameters for the Verilog file
COMPILE_ARGS += -P$(TOPLEVEL).DW=$(DW) -P$(TOPLEVEL).log2_samples=$(log2_samples) -P$(TOPLEVEL).US=$(US)

include $(shell cocotb-config --makefiles)/Makefile.sim
