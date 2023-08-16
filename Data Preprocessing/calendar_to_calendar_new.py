# The purpose of this file is to modify the end_date and start_date columns within the calendar dataset.
# This modification involves converting them into monthly intervals and introducing
# a new column labeled 'month,' where an integer value is assigned to represent the respective month.
# These are stored in a new dataframe 'new_calendar' and saved to a csv.

import datetime

import pandas as pd

routes_speed_distance = pd.read_csv("GTFS data waikato/routes_speed_distance.csv")
calendar= pd.read_csv("GTFS data waikato/calendar.txt")

calendar['start_date'] = pd.to_datetime(calendar['start_date'].astype(str),format="%Y%m%d")

calendar['end_date'] = pd.to_datetime(calendar['end_date'].astype(str),format="%Y%m%d")

new_calendar = pd.DataFrame()

for i in range(len(calendar)):
    start_dates = []

    dt_start = calendar.loc[i,'start_date']
    dt_end = calendar.loc[i,'end_date']

    one_day = datetime.timedelta(1)
    start_dates = [dt_start]
    end_dates = []
    today = dt_start

    while today <= dt_end:
        tomorrow = today + one_day
        if tomorrow.month != today.month:
            start_dates.append(tomorrow)
            end_dates.append(today)
        today = tomorrow

    end_dates.append(dt_end)

    for j in range(len(start_dates)):
        new_row = calendar.loc[i].copy()
        new_row['start_date'] = start_dates[j]
        new_row['end_date'] = end_dates[j]
        new_row['month'] = start_dates[j].month
        new_calendar = new_calendar.append(new_row,ignore_index=True)

new_calendar.to_csv("new_calendar.csv")