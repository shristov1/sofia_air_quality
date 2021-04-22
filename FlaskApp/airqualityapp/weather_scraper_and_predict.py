# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.11.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

import weathercom
import pandas as pd
import matplotlib.pyplot as plt
from tensorflow import keras
from .dataframe_wrangling import is_holiday, is_workday, season
import datetime
import joblib
import plotly.graph_objs as go
import os
import numpy as np

# TODO: Automatically take it from G calendar API
HOLIDAYS = [datetime.date(2020,4,19), datetime.date(2021,1,1), datetime.date(2021,3,3),datetime.date(2020,5,1),
            datetime.date(2020,5,6),datetime.date(2020,5,24),datetime.date(2020,9,6),
            datetime.date(2020,9,22),datetime.date(2020,12,24),datetime.date(2020,12,25),datetime.date(2020,12,26)]

def SetColor(x):
    if(int(x) < 5):
        return "green"
    elif(int(x) >= 5) and (int(x) <= 30):
        return "yellow"
    elif(int(x) > 30):
        return "red"


def load_models():
    model = keras.models.load_model('C:\\Users\\Deya\\Documents\\StansBS\\sofia_air_quality\\FlaskApp\\airqualityapp\\ann_regr_weather.h5')
    sc_regr = joblib.load('C:\\Users\\Deya\\Documents\\StansBS\\sofia_air_quality\\FlaskApp\\airqualityapp\\std_scaler.bin')

    return model, sc_regr


def get_weather():
    # This would be an input to the ANN to estimate the air quality for the next few days
    data = weathercom.getCityWeatherDetails(city='Sofia', queryType="ten-days-data")

    return data


def clean_data() -> list:
    data = get_weather()
    df = pd.read_json(data)
    weather = pd.DataFrame()
    date = pd.DataFrame()

    weather['Temperature'] = df['vt1dailyForecast']['day']['temperature']
    weather['Humidity'] = df['vt1dailyForecast']['day']['humidityPct']

    date['Date'] = pd.to_datetime(df['vt1dailyForecast']['validDate'])

    weather['IsHoliday'] = date['Date'].apply(is_holiday)
    weather['Weekday'] = date['Date'].dt.dayofweek
    weather['Season'] = date['Date'].apply(season)

    return [weather, date]


def predict(weather):

    model, sc_regr = load_models()
    weather = sc_regr.transform(weather)
    prediction = model.predict(weather)
    return prediction


def return_figures():
    all_data = clean_data()
    weather = all_data[0]
    date = all_data[1]
    prediction = predict(weather)

    graph_one = []
    graph_one.append(
      go.Bar(
      x = date.Date.tolist(),
      y = weather.Temperature.tolist(),
      )
    )

    layout_one = dict(title = 'Forecasted temperature for the next 10 days',
                xaxis = dict(title = 'Date',),
                yaxis = dict(title = 'Forecasted temperature'),
                )

    graph_two = []
    graph_two.append(
      go.Bar(
      x = date.Date.tolist(),
      y = weather.Humidity.tolist(),
      )
    )

    layout_two = dict(title = 'Forecasted humidity for the next 10 days',
                xaxis = dict(title = 'Date',),
                yaxis = dict(title = 'Forecasted humidity'),
                )

    graph_three = []
    x_val = date.Date.dt.date
    y_val = np.hstack(prediction).tolist()
    graph_three.append(
        go.Scatter(
            x=x_val.tolist(),
            y=y_val,
            mode='markers',
            marker=dict(color=list(map(SetColor, y_val)))
        )
    )

    layout_three = dict(title = 'Predicted PM 10 concentration for the next 10 days',
                xaxis = dict(title = 'Date'),
                yaxis = dict(title = 'PM 10 concentration, µg/m³'),
                )

    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    figures.append(dict(data=graph_three, layout=layout_three))

    return figures

    #plt.scatter(date['Date'], prediction)
    #plt.grid()
    #plt.xlabel('Date')
    #plt.ylabel('PM 10')
    #plt.show()


if __name__ == '__main__':
    return_figures()