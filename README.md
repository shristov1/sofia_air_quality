# Air Quality in Sofia Regression and Prediction

[![Python application](https://github.com/shristov1/sofia_air_quality/actions/workflows/python-app.yml/badge.svg)](https://github.com/shristov1/sofia_air_quality/actions/workflows/python-app.yml)

[![autopy-lot](https://github.com/shristov1/sofia_air_quality/actions/workflows/notebook_pyer.yml/badge.svg)](https://github.com/shristov1/sofia_air_quality/actions/workflows/notebook_pyer.yml)

### Libraries used:

- weathercom
- joblib
- tensorflow
- scikit
- numpy
- pandas
- seaborn
- matplotlib
- os

### Motivation

I live in Sofia, Bulgaria quite a large portion of the year and have my family here.

Sofia is known to have one of the worst air quality in Europe. This is due to having old cars, people heating themselves with old ways - wood and coal and others. 

I decided to look at the data recorded by sensors.community community and analyze the data to find connections between the external factors and air quality, such as: 

- Is there connection between air quality and time of day and week day
- Is there connection between air quality and season and if there is a holiday
- Is there connection between air quality and weather

### Issues:
- not yet known

### Files in repo
- visualization_and_data_analysis.ipynb - Jupyter notebook with the main portion of the work
- weather_scraper_and_predict.ipynb - Jupyter notebook that loads the weather data and predicts based on the model trained
- dataframe_wrangling.py - support functions for dataset preparation
- download_climate_data.py - this contains functions that help with downloading the data
- std_scaler.bin - standart scaler model
- ann_regr_weather.h5 - ANN trained on historical weather, dates and PM 10 values
- README.md - this readme for the project

### Findings:

1. Air quality is best during lunchtime and worse on Friday and Saturday (as people travel most)
2. Air quality is best in the summer (due to no need of heating) and in holidays (because people travel more and are not in the city)
3. There seems to be a higher correlation between PM10 and PM2.5 particle concentration and humidty rather than temperature.

More written analysis on Medium: https://shristov9.medium.com/when-is-sofia-breathing-the-worst-air-93e31a28e6ca 

And also I would finish the classification analysis on the data in due time. Regression is done and next step is to deploy on a cloud service. 

### Acknowledgment:
- sensors.community
- Stackoverflow
