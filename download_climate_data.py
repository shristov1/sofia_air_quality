# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 16:39:41 2021

This will be used to query an FTP server to download csv data from the sensors of interest. 

@author: sHristov
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
    """
    Function to create a range given start and end dates. 
    Acknowledgment:
    https://stackoverflow.com/questions/1060279/iterating-through-a-range-of-dates-in-python
    """
    
    for n in range(int((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)


def download_data(sensor_name: str, sensor_id: str, start_date = datetime.date(2020, 4, 1)) -> None:
    """
    Function to download data from the sensor.community server and puts it in a data folder. 
    Args:
    sensor_name - name of sensor
    sensor_id - id of sensor

    Returns: 
    None 
    """
    folder_main = os.getcwd()
    data_folder = folder_main + os.sep + 'data' + os.sep

    try:
        os.mkdir(data_folder)
    except FileExistsError:
        pass

    
    # Get data until yesterday - the server is only updated at 00:00 GMT
    end_date = datetime.date.today() - datetime.timedelta(days=1)
    for single_date in daterange(start_date, end_date):

        print('Downloading: ' + str(single_date))
        
        filename = "%s_%s_sensor_%s.csv" % (str(single_date), sensor_name, sensor_id)
        save_name = os.path.join(data_folder, filename)
        

        if os.path.exists(save_name):
            logging.debug(f"{save_name} exists, skipping file")

        else:
            logging.debug("Trying to download...")
            time.sleep(1)
            url = 'https://archive.sensor.community/%s/%s' % (str(single_date), filename)
            req = requests.get(url)
            url_content = req.content
            with open(save_name, 'wb') as csv_file:
                csv_file.write(url_content)
                csv_file.close()


if __name__ == '__main__':
    # code below is used for testing purposes
    sensor_name = 'sds011'
    sensor_id = '6127'
    """ raise HTTPError (urllib.error.HTTPError) if data does not exist"""

    download_data(sensor_name=sensor_name, sensor_id=sensor_id)
