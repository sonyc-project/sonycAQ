# SONYC Air Quality Jupyter Notebooks
This directory houses the analysis notebooks.

The notebooks present represent the most relevant and up-to-date analysis. These notebooks can be used as models for future data analysis, and examples of data that was collected in certain controlled environments for certain periods of time.

[Single-Day Hourly Analysis 1](https://github.com/sonyc-project/sonycAQ/blob/main/notebooks/Single-Day%20Hourly%20Analysis%201.ipynb) imports and concatenates the .csv files from 3.5 hours worth of analysis. It creates simple bar graphs of hourly PM value concentration.

[Single-Day Hourly Analysis 2](https://github.com/sonyc-project/sonycAQ/blob/main/notebooks/Single-Day%20Hourly%20Analysis%202.ipynb) imports and concatenates the .csv files from 7.5 hours worth of analysis. It does the following: 

- Creates bar graphs of certain hourly PM value concentrations. 
- Creates a rolling hourly average PM2.5 value and plots this vs. time. 
- Plots hourly PM2.5 values in a bar graph with treshold lines (values from the literature). 
- Calculates AQI for the day using the data it has (with the acknowledgement that true PM2.5 requires 24 hours worth of data).
    
[Multi-Day Longitudinal Analysis 1](https://github.com/sonyc-project/sonycAQ/blob/main/notebooks/Multi-Day%20Longitudinal%20Analysis%201.ipynb) imports and concatenates the .csv files from 48 hours worth of analysis. It does the following:

 - Creates bar graphs of certain hourly PM value concentrations.
 - Creates bar graphs of certain daily PM value concentrations.
 - Creates rolling hourly average PM values and plots them vs. time.
 - Plots hourly PM values in a bar graph with treshold lines (values from the literature).
 - Plots daily PM values in a bar graph with treshold lines (values from the literature).
 - Calculates the PM2.5 AQI for each day and graphs these values (both with and without treshold lines).
 - Calculates the PM10 AQI for each day and graphs these values (both with and without treshold lines).
