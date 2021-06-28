## Current (as of 06-28-2021) python program for taking a serial reading of the IPS and writing to a csv file every minute
## Author: James Venditto (jmv7849@nyu.edu)
# SONYC - AQ Sensor Project This program reads AQ data from an IPS-7100 sensor attached to the serial port of a
# Raspberry Pi, formatting it and saving it to a .csv file stored in the serial folder.
import serial
import time
from time import strftime
import csv
import re

# Setup Serial Port:
ser = serial.Serial(
	port='/dev/ttyAMA0',
	baudrate=115200,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=1
)

min_count = 0                                       # counts number of minutes for run of program (full program would run indefinitely)

while min_count < 5:                                # this test runs for 5 minutes (5 .csv files produced)
# Write header:
	timestamp = strftime("%Y_%m_%d-%H_%M_%S")
	filename = "test_node-venditto-pm-" + timestamp + ".csv"
	header = ['datetime','PC0.1','PC0.3','PC0.5','PC1.0','PC2.5','PC5.0','PC10','PM0.1','PM0.3','PM0.5','PM1.0','PM2.5','PM5.0','PM10'] 
	with open(filename,'a') as test_header:
		test_writer = csv.writer(test_header)
		test_writer.writerow(header)
	
    sec_count = 0                                   # counts number of seconds for each .csv file (60 seconds = 60 entries per file)

# Write entries for individual .csv files:
	while sec_count < 60:
		data = ser.readline()                       # read data from serial bus
		date_and_time = strftime("%s")              # record time (in seconds since beg. of epoch) of measurement
		data = re.sub('(P(C|M)10,)','',data)        # these lines remove non-numerical string data
		data = re.sub('(P(C|M)\d\S\d,)','',data)
		data = re.sub('P,','',data)
		result = re.split(',',data)                 # splits string into elements that can be written to csv using regex
		with open(filename,'a') as test_data:
			test_writer = csv.writer(test_data)
			row = [date_and_time,result[0],result[1],result[2],result[3],result[4],result[5],
					result[6],result[7],result[8],result[9],result[10],result[11], result[12],result[13]] 
			test_writer.writerow(row)
		time.sleep(1)                               # wait 1 second before next measurement
		sec_count = sec_count + 1

	min_count = min_count + 1
