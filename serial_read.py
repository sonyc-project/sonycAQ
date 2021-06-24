## Author: James Venditto (jmv7849@nyu.edu)
# SONYC - AQ Sensor Project
# This program reads AQ data from an IPS-7100 sensor attached to the serial port of a 
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

# Write header (start of file only):
header = ['datetime','PC0.1','PC0.3','PC0.5','PC1.0','PC2.5','PC5.0','PC10','PM0.1','PM0.3','PM0.5','PM1.0','PM2.5','PM5.0','PM10']
with open('filename.csv','a') as test_data:
	test_writer = csv.writer(test_data)
	test_writer.writerow(header)

count = 0

# Take x number of measurements, save to .csv file with tamp stamp in seconds since epoch:
while count < 100:
	data = ser.readline()
	date_and_time = strftime("%s")
	data = re.sub('(P(C|M)10,)','',data)
	data = re.sub('(P(C|M)\d\S\d,)','',data)
	result = re.split(',',data)
	with open('filename.csv','a') as test_data:
		test_writer = csv.writer(test_data)
		row = [date_and_time,result[0],result[1],result[2],result[3],result[4],result[5],
				result[6],result[7],result[8],result[9],result[10],result[11],
				result[12],result[13]]
		test_writer.writerow(row)

	time.sleep(1)
	count = count + 1
