# Running the Machine Learning Modal with nearby weather station

In this kind of approach we are relying on local weather station to calibrate our AQ_Sensor. As we know that the environment relative humidity and Temperature plays an important factor in sensor calibration due to linear dependency so instead of relying on temperature and relative humidy directly from the sensor. Which may provide false reading due to senor overheating or some failure So to avoid this false calibration of the sensor we are relying on local wether station data for getting Temperature and Relative humidity.

# The Weather Scraper (🌩⛈🌤🌞🌨)

Need High-resolution Weather Data for Analytics or Machine-learning ? Seek no more.

## Overview

The Weather Scraper downloads high-resolution weather data (often 5 min. intervals) from Wunderground's public weather stations around the world for you.

#### TLDR

```python
python weather_scraper.py
```

### How to run TWS?

First, find the weather stations you are looking for.  
Then you just have to update 2 config files before running TWS.

1. Go to https://www.wunderground.com/wundermap and zoom in to your location  
   🌞 Click on a weather station and then click on the **Station ID** (the Station Summary page will open)  
   🌞 Open and copy all Station ID URLs you need

2. Set the weather*station urls inside **stations.txt**  
   🌞 \_one url per line!*

3. Inside **config.py**  
   🌞 Set the date-range you want to download your data from  
   🌞 Set the unit system you need (metric / imperial)  
   🌞 Set FIND_FIRST_DATE to true if you want the weather scraper to use binary search to search for the first date with data, starting from START_DATE

If you want to download data from 2020/5/1 to 2020/6/1 in metric units your config.py will look like this:

```python

from datetime import date

# Set Date format like: YYYY, MM, DD
START_DATE = date(2020, 5, 1)
END_DATE = date(2020, 6, 1)
# set to "metric" or "imperial"
UNIT_SYSTEM = "metric"

# Automatically find first date where data is logged
FIND_FIRST_DATE = False
```

Now you are read to run your downloads:

```sh
$ python weather_scraper.py
```

Wait until TWS finishes writing your data to files with this naming pattern **_station_name.csv_**!

You resulting CSV file will look something like this (if you give it a nice format)

![CSV example](https://raw.githubusercontent.com/Karlheinzniebuhr/the-weather-scraper/master/resources/csv.JPG)

### Running Scraper and ML Modal from a single script

You can directly run the weather scraper and the machine learning modal from a single file by:

```sh
running with_weather_ML.ipynb notebook
```

The script first find the weather .csv file if it found's one then it will delete that csv file and redownload the file to match the timestamp of the Machine learnig modal.

Also, by relying on local weather data for sensor calibration it was seen that there is approx 92% dominance of the AQ_sensor data compared to Temperature and Relative Humidity data.

### Calibration of sensors in an Uncontrolled Environment under Sounds of New York City Project.

The objective of the project is to calibrate an Air Quality Sensor ie AQSensor by using different method such as _Machine Learning_ and _Neural Network_:

1. Multiple Linear Regression (MLR)
2. K-Nearest Neighbour (KNN)
3. Random Forest (RF)
4. Kernel Regression (KR)
5. Gaussian Process (GP)
6. Support Vector Regression (SVR)
7. Neural Netwok (NN)

## About

This project is developed under New York University at Center of Urban Sciences and Progress.

The Data is organized as follows:

1. RefSt: Reference value of highly calibrated Sensor Praxis_Data_pm2.5.
2. Sensor_01: Praxis_Data_pm2.5 Sensor which need to be calibrated.
3. Temp: Temperature Data from from vicinity station.
4. RelHum: Relative Humidity from vicinity station.

## Data Calibration

A data calibration process was done using the network of three sensor data (_Canary_Data_, _RelHum_, _Temp_) will be trained against reference data _RefSt_ using different regression algorithm.

For this process, the main dataset is splitted into 60% training set and 40% test set. Given that the dataset contains data from 50 days with 1 min timestamp. The **data does have sesonality**, This is why data split is made without shuffling.

To check performance and later compare them, some **regression loss function** values are calculated for each method:

- _Coefficient of determination_ R<sup>2</sup>: determines to what extent the variance of one variable explains the variance of the second variable
- _Root-mean-square error_ RMSE: the standard deviation of the residuals (prediction errors)
- _Mean absolute error_ MAE: a measure of errors between paired observations expressing the same phenomenon
