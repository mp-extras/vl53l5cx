# used to build a binary blob firmware file for the sensor's MCU
VL53L5CX_ULD_DIR := /home/mark/Projects/vl53l5cx/VL53L5CX_ULD_driver_1.1.0

vl53l5cx/%.mpy: vl53l5cx/%.py
	mpy-cross -O2 $^
	mpremote cp $@ :lib/$@

vl_fw.bin: fw_file
	@echo generating firmware bin file from C header file ...
	@./fw_file

fw_file: fw_file.c  $(VL53L5CX_ULD_DIR)/VL53L5CX_ULD_API/inc/vl53l5cx_buffers.h
	gcc -Wall -I $(VL53L5CX_ULD_DIR)/VL53L5CX_ULD_API/inc/ -I $(VL53L5CX_ULD_DIR)/Platform -o fw_file fw_file.c

install: vl53l5cx/__init__.mpy vl53l5cx/mp.mpy vl53l5cx/_config_file.mpy
	@echo copying firmware ...
	# @mpremote cp vl53l5cx/vl_fw_config.bin :lib/vl53l5cx/vl_fw_config.bin

clean:
	@echo cleaning ...
	@rm -f vl_fw.bin *.mpy fw_file vl53l5cx/*.mpy
