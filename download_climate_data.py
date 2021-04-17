# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 16:39:41 2021

@author: Deya
"""

import os
import time
import datetime
import logging
import gzip
import typing
import urllib.error
import urllib.request
import requests
import bs4

import numpy as np
import pandas as pd


def daterange(start_date: datetime.datetime, end_date: datetime.datetime) -> typing.Iterable[datetime.datetime]:
    """https://stackoverflow.com/questions/1060279/iterating-through-a-range-of-dates-in-python"""
    for n in range(int((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)


folder_main = os.getcwd()
data_folder = folder_main + os.sep + 'data' + os.sep

sensor_name = 'sds011'
sensor_id = '6127'
""" raise HTTPError (urllib.error.HTTPError) if data does not exist"""
#date_str =datetime.date.today().strftime('%y-%m-%d')

start_date = datetime.date(2020, 4, 1)
end_date = datetime.date(2021, 1, 2)
for single_date in daterange(start_date, end_date):

    print('Downloading: ' + str(single_date))
    
    filename = "%s_%s_sensor_%s.csv" % (str(single_date), sensor_name, sensor_id)
    save_name = os.path.join(data_folder, filename + '.gz')

    if os.path.exists(save_name):
        logging.debug("%s exists, loading from file" % save_name)
        with gzip.open(save_name, 'r') as f:
            data = f.read()
    else:
        logging.debug("Trying to download...")
        time.sleep(1)
        url = 'https://archive.sensor.community/%s/%s' % (str(single_date), filename)
        data = urllib.request.urlopen(url).read()
    
        with gzip.open(save_name, 'w+') as f:
            f.write(data)
