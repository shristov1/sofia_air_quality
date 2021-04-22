import pandas as pandas
import matplotlib.pyplot as plt
import datetime

"""
This file will hold functions that I find useful for data wrangling and sorting of pandas dataframes. 

Author: sHristov
"""

# TODO: Automatically take it from G calendar API
HOLIDAYS = [datetime.date(2020,4,19), datetime.date(2021,1,1), datetime.date(2021,3,3),datetime.date(2020,5,1),
            datetime.date(2020,5,6),datetime.date(2020,5,24),datetime.date(2020,9,6),
            datetime.date(2020,9,22),datetime.date(2020,12,24),datetime.date(2020,12,25),datetime.date(2020,12,26)]


def mean_print_plot(df, category: str, data_col1: str, data_col2: str) -> None:
    """Function which prints the mean of each category in a data column and plots the difference between the 2 datasets
    
    Parameters: 
    df: data frame
    category: category name
    data_col1: data to calculate mean on
    data_col2: data to calculate mean on
    main_category: used to further filter the data based on a master category
    
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


def is_workday(x):
    """ Returns if day is workday"""
    if x <= 4:
        return 1
    else:
        return 0


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


def is_holiday(x):
    """ Returns if it is holiday if date is 3 days around a holiday"""
    for holiday in HOLIDAYS:
        if (x >= holiday-datetime.timedelta(days=3)) and (x <= holiday + datetime.timedelta(days=3)):
            return 1
        else:
            return 0
