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

time.sleep(10)                                          # sleep to let port initialize (datasheet rec. >5 sec)

error_count = 0                                         # counter variable to determine if serial port is malfunctioning

min_count = 0                                           # minute conter variable (not used in final release)

while min_count < 5:

	if (error_count != 0):                              # if previous run detected malfunction in serial port, reset it
		ser = serial.Serial(
        		port='/dev/ttyAMA0',
                baudrate=115200,
        		parity=serial.PARITY_NONE,
        		stopbits=serial.STOPBITS_ONE,
        		bytesize=serial.EIGHTBITS,
        		timeout=1
		)

		time.sleep(10)                                  # sleep to let port reinitialize 

		error_count = 0                                 # reset error counter
    
    # setup new .csv file:
	timestamp = strftime("%Y_%m_%d-%H_%M_%S")
	filename = "test_node-venditto-pm-" + timestamp + ".csv"
	header = ['datetime','PC0.1','PC0.3','PC0.5','PC1.0','PC2.5','PC5.0','PC10','PM0.1','PM0.3','PM0.5','PM1.0','PM2.5','PM5.0','PM10'] 
	with open(filename,'a') as test_header:
		test_writer = csv.writer(test_header)
		test_writer.writerow(header)
	
    sec_count = 0                                       # couter variable for each run (each second)

	# while 1 minute:
	while sec_count < 60:
		data = ser.readline()                           # read the serial bus
		if (data[0] != 'P' and data[1] != 'C'):         # if data is wrong (corrupted, nonexistant) increment error counter, don't write to file
			error_count = error_count + 1
		else:                                           # if data is acceptable, record to .csv
			error_count = 0
			date_and_time = strftime("%s")
			data = re.sub('(P(C|M)10,)','',data)        # regex functions format data by removing non numeric characters (beside commas)
			data = re.sub('(P(C|M)\d\S\d,)','',data)
			result = re.split(',',data)
			with open(filename,'a') as test_data:
				test_writer = csv.writer(test_data)
				row = [date_and_time,result[0],result[1],result[2],result[3],result[4],result[5],
						result[6],result[7],result[8],result[9],result[10],result[11], result[12],result[13]] 
				test_writer.writerow(row)

		time.sleep(1)                                   # wait 1 second (measurments are 1/sec)
		sec_count = sec_count + 1

	min_count = min_count + 1