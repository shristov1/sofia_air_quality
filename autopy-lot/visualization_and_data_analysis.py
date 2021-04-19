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

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from download_climate_data import download_data
import os
import datetime


# We are only interested in sensors with the following parameters: (sensor_name = sds011, sensor_id = 6127) and (sensor_name = bme280, sensor_id = 6128).

def part_day(x):
    """ Returns part of day based on the timestamp hour """
    x = x.hour
    if (x > 4) and (x <= 8):
        return 1
    elif (x > 8) and (x <= 12):
        return 2
    elif (x > 12) and (x <= 14):
        return 3
    elif (x > 14) and (x <= 18):
        return 4
    elif (x > 18) and (x <= 22):
        return 5
    else:
        return 6


def season(x):
    """Returns season based on month"""
    x = x.month
    if (x > 3) and (x <= 6):
        return 1
    elif (x > 6) and (x <= 9):
        return 2
    elif (x > 9) and (x <= 11):
        return 3
    else:
        return 4


def is_workday(x):
    """ Returns if day is workday"""
    if x <= 4:
        return 1
    else:
        return 0


def mean_print_plot(df, category: str, data_col1: str, data_col2: str) -> None:
    """Function which prints the mean of each category in a data column and plots the difference between the 2 datasets
    
    Parameters: 
    df: data frame
    category: category name
    data_col1: data to calculate mean on
    data_col2: data to calculate mean on
    
    Returns: 
    None
    
    """
    
    print(f"P1 data stats: {df.groupby([category]).mean()[data_col1].sort_index()}")
    print('------------------------------------------------')
    print(f"P2 data stats: {df.groupby([category]).mean()[data_col2].sort_index()}")
    
    plt.plot(df.groupby([category]).mean()[data_col1].sort_index(), label='P1')
    plt.plot(df.groupby([category]).mean()[data_col2].sort_index(), label='P2')
    plt.title(f'Mean of {data_col1} and {data_col2} per {category} category')
    plt.legend()
    plt.grid()


def is_p1_high(x):
    if x > 35:
        return 1
    else:
        return 0


def is_holiday(x):
    """ Returns if it is holiday if date is 3 days around a holiday"""
    for holiday in HOLIDAYS:
        if (x >= holiday-datetime.timedelta(days=3)) and (x <= holiday+datetime.timedelta(days=3)):
            return 1
        else:
            return 0


# Also, we are going to create a list with all public holidays:  
# Date	Holiday	Official Name  
# 1 January	New Year's Day   
# 3 March	Liberation Day  
# 1 May	International Workers' Day  
# 6 May	Saint George's Day  
# 24 May	Bulgarian Education and Culture and Slavonic Literature Day  
# 6 September	Unification Day  
# 22 September	Independence Day  
# 24 December	Christmas Eve  
# 25 & 26 December	Christmas Day  
# Moveable	Orthodox Good Friday, Holy Saturday & Easter  

HOLIDAYS = [datetime.date(2020,4,19), datetime.date(2021,1,1), datetime.date(2021,3,3),datetime.date(2020,5,1),
            datetime.date(2020,5,6),datetime.date(2020,5,24),datetime.date(2020,9,6),
            datetime.date(2020,9,22),datetime.date(2020,12,24),datetime.date(2020,12,25),datetime.date(2020,12,26)]

START_DATE = datetime.date(2020,4,1)   # start time for the analysis

# ### Data download now

download_data(sensor_name='sds011', sensor_id=6127)
download_data(sensor_name='bme280', sensor_id=6128)

# #### We have all the data, let us now load the data in dataframe

file_list = os.listdir('./data/')

date_list = set([file.split('_')[0] for file in file_list]) # get unique dates

df = pd.DataFrame()

for date in date_list:
    for file in file_list:
        if file.find(date) != -1:
            if file.find('bme280') != -1:
                df_temp_1 = pd.read_csv('./data/'+file, sep=';')
                df_temp_1.timestamp = pd.to_datetime(df_temp_1.timestamp, errors='ignore', infer_datetime_format=True)
            elif file.find('sds011') != -1:
                df_temp_2 = pd.read_csv('./data/'+file, sep=';')
                df_temp_2.timestamp = pd.to_datetime(df_temp_2.timestamp, errors='ignore', infer_datetime_format=True)
            
        df_1 = pd.merge_asof(df_temp_1, df_temp_2, on='timestamp', direction='nearest', tolerance=datetime.timedelta(seconds=20), allow_exact_matches=False)
        df_1.drop(['altitude', 'pressure', 'durP2', 'ratioP2', 'durP1', 'ratioP1', "ratioP2",
                  'sensor_id_x', 'sensor_type_x', 'location_x', 'lat_x', 'lon_x', 'pressure_sealevel',
                  'sensor_id_y', 'sensor_type_y', 'location_y', 'lat_y','lon_y'], axis=1, inplace=True);
        df_1.dropna(inplace=True)
    df = pd.concat([df, df_1])

df.reset_index(inplace=True)
df.drop('index', axis=1, inplace=True)

df['IsHoliday'] = df['timestamp'].apply(is_holiday) 
df['PartDay'] = df['timestamp'].apply(part_day)

df['WeekDay'] = df['timestamp'].dt.dayofweek

df['IsWorking'] = df['WeekDay'].apply(is_workday)

df['Season'] = df['timestamp'].apply(season)

# Check if the P1 and P2 values are higher in any part of the day or if it is a holiday.

mean_print_plot(df, category='IsHoliday', data_col1='P1', data_col2='P2')

mean_print_plot(df, category='WeekDay', data_col1='P1', data_col2='P2')

mean_print_plot(df, category='PartDay', data_col1='P1', data_col2='P2')

mean_print_plot(df, category='Season', data_col1='P1', data_col2='P2')

# ### As we see there are correlations between the season, week day, time of day and holidays and the air quality. 
# ##### I will now check with a seaborn correlation plot

sns.heatmap(df.corr(), annot=True)

# Strangly enough there seems to be a correlation also between the humidity and the air quality, but not that much with temperature.

# ### Regression
# ##### I think that this problem may be best generalized with a random forest model. First I will start with a regressor, then I will use a classifier

from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler

X = df[['temperature', 'humidity', 'IsHoliday', 'WeekDay', 'Season']]
y = df['P1']
today = [1, 100, 0, 6, 1]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3)

sc_regr = StandardScaler()
X_train = sc_regr.fit_transform(X_train)
X_test = sc_regr.transform(X_test)
today = sc_regr.transform([today])

regr = RandomForestRegressor()
regr_svm = SVR()

regr.fit(X_train, y_train)
regr_svm.fit(X_train, y_train)

regr.predict(today)

regr_svm.predict(today)

y_pred_svm = regr_svm.predict(X_test)

# plt.plot(y_test)
# plt.plot(y_pred_svm)

df['HighP1'] = df['P1'].apply(is_p1_high)

# ### Now I will run a classification RF model

from sklearn.ensemble import RandomForestClassifier

y = df['HighP1']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3)

classifier = RandomForestClassifier()

classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)

print(accuracy_score(y_test, y_pred))

print(confusion_matrix(y_test,y_pred))

print(classification_report(y_test, y_pred))


classifier.predict_proba([today])
regr.predict([today])

regr.feature_importances_

classifier.feature_importances_

# Results are not great - this may be due to overfitting of the clean air data as we have roughly 5 times more data for that case

from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
today = [1, 100, 0, 6, 1]
sc = StandardScaler()

classifier_svc = SVC()

X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)
today = sc.transfort([today])
classifier_svc.fit(X_train, y_train)

y_pred_svc = classifier_svc.predict(X_test)

print(classification_report(y_test, y_pred_svc))

classifier_svc.predict(today)


