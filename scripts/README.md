# SONYC AQ Python Script Repository

Repository housing current scripts to be used with IPS-7100 - Raspberry Pi interface.

[AQ_test5.py](https://github.com/sonyc-project/sonycAQ/blob/main/scripts/AQ_test5.py) - This is the current script for collecting AQ data. It collects AQ information every
second, storing it in a .csv file. New files are created approximately every minute, so long as the data is readable. The script is capable of detecting when the data bus
is unreadable, or when data is otherwise formatted incorrectly. It will abandon the current .csv file when errors are detected, and it will start a new .csv file only when the errors are determined to be fixed. 

[serial_write.py](https://github.com/sonyc-project/sonycAQ/blob/main/scripts/serial_write.py) - This script is a simple prototype that can be used to write commands to the
IPS-7100 from the Raspberry Pi. These commands can include setting whether or not the output data string includes the network serial number and product key, or setting the units the data is displayed in. The full list of commands can be found in the [IPS datasheet](https://github.com/sonyc-project/sonycAQ/blob/main/docs/IPS-Datasheet-V1.0.2.pdf). 
