# SONYC Air Quality (sonycAQ)
Repository to house the code and related docs for the air quality (AQ) aspects of the [Sounds Of New York City (SONYC) project](https://wp.nyu.edu/sonyc).

The AQ sensor chosen is the [Piera IPS-7100 Intelligent Particle Sensor](https://www.pierasystems.com/products/piera-7100-intelligent-particle-sensor) which communiactes via UART with the SONYC project's Raspberry Pi 4B based noise sensor.

![image](https://user-images.githubusercontent.com/86373439/128935455-52568d5b-1691-46e3-8aee-3af3ae30c94b.png)

## Introduction - Why is AQ part of SONYC?
Air pollutants, including particulate matter (PM's), particularly PM2.5, are a significant health concern in urban areas such as New York City. The NYC Department of Health estimates approximately 3,000 people die each year due to PM2.5-related illnesses in the city, and approximately 8,000 more hospital visits can be linked to dangerous PM2.5 exposure. [Maps](https://www1.nyc.gov/assets/doh/downloads/pdf/eode/eode-air-quality-impact.pdf) from a study by the Department of Health show that the distribution of PM2.5-related medical incidents is not even across neighborhoods, and is elevated with higher poverty rates. This shows that particulate matter air pollution is a community-based problem, that may have a community-based solution.

The following tables from the aforementioned [Department of Health study](https://www1.nyc.gov/assets/doh/downloads/pdf/eode/eode-air-quality-impact.pdf) illustrate the danger of NYC PM2.5 concentrations and showcase the exacerbated risk to communities with high poverty rates. Further figures are available at the source.

![image](https://user-images.githubusercontent.com/86373439/128933800-203ed878-9706-475b-8545-4675aa4cc693.png)

![image](https://user-images.githubusercontent.com/86373439/128934092-9049ec9c-7452-40d1-ad3f-a3150b4776e7.png)

Images courtesy of the NYC Department of Health and Mental Hygiene.

SONYC has spent years working with citizen-science based approaches to the issue of noise pollution in New York City, and we are now capable of expanding that infrastructure to examine air pollution. The availablility of reasonably-priced and scalable devices such as the IPS-7100 will allow us to eventually create a wide network of citizen-based  collectors of air pollutant levels and air quality in New York City neighborhoods.

We are particularly interested in examining air pollution due to the potential correlation between it and noise pollution. Some research into this correlation has been done, but neither in NYC residential settings, nor through a citizen-based initiative. SONYC is in a unique position to leverage existing sound-collecting apparatus and community relationships towards examining this correlation. More data regarding this correlation may lead to better understandings of links between air or noise pollution and certain health conditions, and can help city agencies and community groups to better devote resources to neighborhoods with pollution problems.

Additionally, SONYC's existing app for delivering sound data to residents in real time and requesting their qualitative analysis of sound quality can be modified to perform the same functions with air quality. AQ data processed by the new code can be delivered into the app and presented in real time, in a manner suitable for a non-specialist audience. It can also be used as a means for collecting qualitative data, allowing us to link quantitative analysis with qualitative feedback.


## Data Formatting Information

### Output String Information
Output information from the IPS is delivered to the Pi as a string. This string contains the particle count and particle mass for the particle sizes measured by the sensor (PM0.1, PM0.3, PM0.5, PM1.0, PM2.5, PM5.0, and PM10) in the units the sensor is set to. Under default settings, the count is measured in # of particles per liter (#/L), and the mass in micrograms per cubic meter (ug/m^3). Also under default settings, the string terminates with the sensor's serial number and network key.

### Example Unformatted Output String
`PC0.1,###,PC0.3,###,PC0.5,###,PC1.0,###,PC2.5,###,PC5.0,###,PC10,###,PM0.1, #.####,PM0.3, #.####,PM0.5, #.####,PM1.0, #.####,PM2.5, #.####,PM5.0, #.####,PM10, #.####,IPS-S-#########,abcdefg######=`

### CSV File Format
CSV files are generated once every minute, and a reading is taken every second, corresponding to a new row in the current file. Each CSV file is named with the following format: `sonycnode-xxxxxxxxxxxx-pm-YYYY_MM_DD-HH_MM_SS.csv`. The first line in each file is a header, and all subsequent lines represent one of the measurements, with the first column as the timestamp (in seconds since the beginning of the epoch), and the subsequent columns representing PC0.1 - PC10, and PM0.1 - PM10.

### CSV File Header
`datetime,PC0.1,PC0.3,PC0.5,PC1.0,PC2.5,PC5.0,PC10,PM0.1,PM0.3,PM0.5,PM1.0,PM2.5,PM5.0,PM10`


## Previous Development Stages (Completed)

1. Wire up sensor to Raspberry Pi via UART and create Python script to read its output [x]
2. Parse output string and write to CSV file with a measurment per second [x]
3. Create a new CSV file every minute with each containing a header row and a minutes worth of measurements - each file should be named with the following format: `sonycnode-xxxxxxxxxxxx-pm-YYYY_MM_DD-HH_MM_SS.csv` [x]
4. Collect a few days worth of continuous data from the sensor nearby an open window [x]
5. Create a Jupyter Notebook in this repository and plot the data using matplotlib [x]


## Script Information

The current Python script used to record data and write to .csv files is called [AQ_test5.py](https://github.com/sonyc-project/sonycAQ/blob/main/scripts/AQ_test5.py) and is stored in the `scripts` folder.

The program first must initialize the serial port on the Raspberry Pi with the settings of the IPS-7100. The rest of the code is contained in an infinite `while` loop. If the program detects the bus is unreadable, or has wrongly formatted data, it will not create a new .csv file and will wait until it has proper data. Otherwise, it will create a new .csv file with the appropriate timestamp, and then write new rows of data every second for one minute. In general, each .csv file is 1 minute worth of data. However, if during this time the bus becomes unreadable or improper data is detected, the program will exit the 1 minute loop and wait for proper data, upon which it begins a new .csv file.

Assuming proper data, the timestamp is recorded in `yyyy-mm-dd-hh-MM-ss` format and used to make the .csv file's title. The header is then written using regex functions. The counter variable,`sec_count`, which ensures 60 entries per file, is initialized.

The second `while` loop keeps track of the entries (or number of seconds) written. If the bus is readable, data is collected and checked for proper formatting. If correct, the current time in seconds from the epoch is recorded. It then uses regex functions to format the string, removing non-numerical characters apart from commas separating numerical values. Next it uses a regex function that splits the values into individual elements of an array (the commas allow demarcation of the values). This array, along with the current time recorded prior, are used to write a new row in the current .csv file. The Raspberry Pi then sleeps for 1 second, before finally incrementing the counter variable and returning to the start of the loop.

This script uses the `serial`, `time`, `csv`, and `re` Python libraries. 
