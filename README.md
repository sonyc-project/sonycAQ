# SONYC Air Quality (sonycAQ)
Repository to house the code and related docs for the air quality (AQ) aspects of the [Sounds Of New York City (SONYC) project](https://wp.nyu.edu/sonyc).

TODO: image of IPS-7100

The AQ sensor chosen is the [Piera IPS-7100 Intelligent Particle Sensor](https://www.pierasystems.com/products/piera-7100-intelligent-particle-sensor) which communiactes via UART with the SONYC project's Raspberry Pi 4B based noise sensor.

# Output String Information
Output information from the IPS is delivered to the Pi as a string. This string contains the particle count and particle mass for the particle sizes measured by the sensor (PM0.1, PM0.3, PM0.5, PM1.0, PM2.5, PM5.0, and PM10) in the units the sensor is set to. Under default settings, the count is measured in # of particles per liter (#/L), and the mass in micrograms per cubic meter (ug/m^3). Also under default settings, the string terminates with the sensor's serial number and network key.

# Example Unformatted Output String
`PC0.1,###,PC0.3,###,PC0.5,###,PC1.0,###,PC2.5,###,PC5.0,###,PC10,###,PM0.1, #.####,PM0.3, #.####,PM0.5, #.####,PM1.0, #.####,PM2.5, #.####,PM5.0, #.####,PM10, #.####,IPS-S-#########,abcdefg######=`

TODO: info on output CSV format

## Development stages

1. Wire up sensor to Raspberry Pi via UART and create Python script to read its output [x]
2. Parse output string and write to CSV file with a measurment per second [x]
3. Create a new CSV file every minute with each containing a header row and a minutes worth of measurements - each file should be named with the following format: `sonycnode-xxxxxxxxxxxx-pm-YYYY_MM_DD-HH_MM_SS.csv` [x]
4. Collect a few days worth of continuous data from the sensor nearby an open window [ ]
5. Create a Jupyter Notebook in this repository and plot the data using matplotlib [ ]

## Script information

TODO: describe script operation
TODO: add comments to scripts describing major lines
