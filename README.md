# SONYC Air Quality (sonycAQ)
Repository to house the code and related docs for the air quality (AQ) aspects of the [Sounds Of New York City (SONYC) project](https://wp.nyu.edu/sonyc).

The AQ sensor chosen is the [Piera IPS-7100 Intelligent Particle Sensor](https://www.pierasystems.com/products/piera-7100-intelligent-particle-sensor) which communiactes via UART with the SONYC project's Raspberry Pi 4B based noise sensor.

### Output String Information
Output information from the IPS is delivered to the Pi as a string. This string contains the particle count and particle mass for the particle sizes measured by the sensor (PM0.1, PM0.3, PM0.5, PM1.0, PM2.5, PM5.0, and PM10) in the units the sensor is set to. Under default settings, the count is measured in # of particles per liter (#/L), and the mass in micrograms per cubic meter (ug/m^3). Also under default settings, the string terminates with the sensor's serial number and network key.

### Example Unformatted Output String
`PC0.1,###,PC0.3,###,PC0.5,###,PC1.0,###,PC2.5,###,PC5.0,###,PC10,###,PM0.1, #.####,PM0.3, #.####,PM0.5, #.####,PM1.0, #.####,PM2.5, #.####,PM5.0, #.####,PM10, #.####,IPS-S-#########,abcdefg######=`

### CSV File Format
CSV files are generated once every minute, and a reading is taken every second, corresponding to a new row in the current file. Each CSV file is named with the following format: `sonycnode-xxxxxxxxxxxx-pm-YYYY_MM_DD-HH_MM_SS.csv`. The first line in each file is a header, and all subsequent lines represent one of the measurements, with the first column as the timestamp (in seconds since the beginning of the epoch), and the subsequent columns representing PC0.1 - PC10, and PM0.1 - PM10.

### CSV File Header
`datetime,PC0.1,PC0.3,PC0.5,PC1.0,PC2.5,PC5.0,PC10,PM0.1,PM0.3,PM0.5,PM1.0,PM2.5,PM5.0,PM10`

## Development stages

1. Wire up sensor to Raspberry Pi via UART and create Python script to read its output [x]
2. Parse output string and write to CSV file with a measurment per second [x]
3. Create a new CSV file every minute with each containing a header row and a minutes worth of measurements - each file should be named with the following format: `sonycnode-xxxxxxxxxxxx-pm-YYYY_MM_DD-HH_MM_SS.csv` [x]
4. Collect a few days worth of continuous data from the sensor nearby an open window [x]
5. Create a Jupyter Notebook in this repository and plot the data using matplotlib [x]

## Script information

The current Python script used to record data and write to .csv files is called `AQ_test5.py` and is stored in the `scripts` folder.

The program first must initialize the serial port on the Raspberry Pi with the settings of the IPS-7100. The rest of the code is contained in an infinite `while` loop. If the program detects the bus is unreadable, or has wrongly formatted data, it will not create a new .csv file and will wait until it has proper data. Otherwise, it will create a new .csv file with the appropriate timestamp, and then write new rows of data every second for one minute. In general, each .csv file is 1 minute worth of data. However, if during this time the bus becomes unreadable or improper data is detected, the program will exit the 1 minute loop and wait for proper data, upon which it begins a new .csv file.

Assuming proper data, the timestamp is recorded in `yyyy-mm-dd-hh-MM-ss` format and used to make the .csv file's title. The header is then written using regex functions. The counter variable,`sec_count`, which ensures 60 entries per file, is initialized.

The second `while` loop keeps track of the entries (or number of seconds) written. If the bus is readable, data is collected and checked for proper formatting. If correct, the current time in seconds from the epoch is recorded. It then uses regex functions to format the string, removing non-numerical characters apart from commas separating numerical values. Next it uses a regex function that splits the values into individual elements of an array (the commas allow demarcation of the values). This array, along with the current time recorded prior, are used to write a new row in the current .csv file. The Raspberry Pi then sleeps for 1 second, before finally incrementing the counter variable and returning to the start of the loop.

This script uses the `serial`, `time`, `csv`, and `re` Python libraries. 
