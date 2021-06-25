# SONYC Air Quality (sonycAQ)
Repository to house the code and related docs for the air quality (AQ) aspects of the [Sounds Of New York City (SONYC) project](https://wp.nyu.edu/sonyc).

TODO: image of IPS-7100

The AQ sensor chosen is the [Piera IPS-7100 Intelligent Particle Sensor](https://www.pierasystems.com/products/piera-7100-intelligent-particle-sensor) which communiactes via UART with the SONYC project's Raspberry Pi 4B based noise sensor.

TODO: info on message format

TODO: info on output CSV format

## Development stages

1. Wire up sensor to Raspberry Pi via UART and create Python script to read its output [x]
2. Parse output string and write to CSV file with a measurment per second [x]
3. Create a new CSV file every minute with each containing a header row and a minutes worth of measurements - each file should be named with the following format: `sonycnode-xxxxxxxxxxxx-pm-YYYY_MM_DD-HH_MM_SS.csv` [ ]
4. Collect a few days worth of continuous data from the sensor nearby an open window [ ]
5. Create a Jupyter Notebook in this repository and plot the data using matplotlib [ ]

## Script information

TODO: describe script operation
TODO: add comments to scripts describing major lines
