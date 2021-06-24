## Author: James Venditto (jmv7849@nyu.edu)
# SONYC - AQ Sensor Project
# This program writes an instruction from the Raspberry Pi to the
# IPS-7100 AQ Sensor on the pi's serial port. It can be used to 
# change the settings according to the datasheet.

import serial
import time
from time import strftime

# Setup serial port:
ser = serial.Serial(
        port='/dev/ttyAMA0',
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)

# Write to the serial bus to change the IPS' settings:
ser.write("$Wazure=1\r\n")

# Test to see if it worked (can't have both in same run):
#data = ser.readline()
#print(data)
