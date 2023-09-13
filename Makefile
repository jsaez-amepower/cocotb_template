# Makefile

SIM ?= icarus
TOPLEVEL_LANG ?= verilog

widtha ?= 18
widthb ?= 18
widthp ?= 36
pipeline ?= 6
us ?= 1

VERILOG_SOURCES = multiplier.v
# use VHDL_SOURCES for VHDL files

# TOPLEVEL is the name of the toplevel module in your Verilog or VHDL file
TOPLEVEL = multiplier

# MODULE is the basename of the Python test file
MODULE = tester

# Output to file
SIM_ARGS=-l$(TOPLEVEL)_stdout.log

# Parameters for the Verilog file
COMPILE_ARGS += -P$(TOPLEVEL).widtha=$(widtha) -P$(TOPLEVEL).widthb=$(widthb) -P$(TOPLEVEL).widthp=$(widthp) -P$(TOPLEVEL).pipeline=$(pipeline) -P$(TOPLEVEL).us=$(us)

include $(shell cocotb-config --makefiles)/Makefile.sim
