## Author: James Venditto (jmv7849@nyu.edu)
# Up to date as of Jul. 8, 2021
# SONYC - AQ Sensor Project 
# This program reads AQ data from an IPS-7100 sensor attached to the serial port of a
# Raspberry Pi, formatting it and saving it to a .csv file stored in the serial folder. If the sensor is disconnected,
# the program stops writing to the .csv file and waits until it determines the sensor is functioning normally, starting 
# a fresh new .csv file.

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

time.sleep(10)                                              # wait for stable data

sec_count = 0                                               # initialize counter variable

while 1:
    if (ser.readable()):                                        # only go ahead if bus is readable
    
        data = ser.readline()
        data_test = re.findall('(P(C|M)\d\S\d,)',data)          # test if data formatted correctly (not printing boot information)
        if (data == ""):                                        # null char = sensor disconnected - do nothing
            pass
        elif (len(data_test) >= 2):                             # data formatted correctly - create new csv
            timestamp = strftime("%Y_%m_%d-%H_%M_%S")
            filename = "test_node-venditto-pm-" + timestamp + ".csv"
            header = ['datetime','PC0.1','PC0.3','PC0.5','PC1.0','PC2.5','PC5.0','PC10','PM0.1','PM0.3','PM0.5','PM1.0','PM2.5','PM5.0','PM10']
            with open(filename,'a') as test_header:
                test_writer = csv.writer(test_header)
                test_writer.writerow(header)
            sec_count = 0

            # "while 1 minute":
            while sec_count < 60:
                if (ser.readable()):                                # only go ahead if bus is readable
                    data = ser.readline()
                    data_test = re.findall('(P(C|M)\d\S\d,)',data)
                    if (data == ""):                                # sensor is disconnected - stop writing to this csv
                        break
                    elif (len(data_test) >= 2):                     # data good - write
                        date_and_time = strftime("%s")
                        data = re.sub('(P(C|M)10,)','',data)        # use regex functions to format properly for csv, remove alphabetical characters
                        data = re.sub('(P(C|M)\d\S\d,)','',data)
                        result = re.split(',',data)
                        with open(filename,'a') as test_data:
                            test_writer = csv.writer(test_data)
                            row = [date_and_time,result[0],result[1],result[2],result[3],result[4],result[5],
                                    result[6],result[7],result[8],result[9],result[10],result[11], result[12],result[13]] 
                            test_writer.writerow(row)
                        time.sleep(1)                               # separate data by 1 second
                        sec_count = sec_count + 1
                    else:                                           # sensor is still booting up or data corrupted - stop writing to file
                        break
                else:                                           # bus is unreadable, go back to top of loop and don't use read function
                    break
                    
        else:                                                   # sensor is still booting up or data corrupted - do nothing
            pass
    
    else:
        time.sleep(5)                                           # sleep for 5 secs if bus is unreadable