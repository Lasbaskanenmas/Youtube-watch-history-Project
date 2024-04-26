### Functions
import pandas as pd
import numpy as np
import calendar
import datetime

# Splits the subtitle column into two new columns; channel_name and channel_url
def split_subtitles(row): 
    subtitles = row.get('subtitles', [{}])
    if isinstance(subtitles, list) and subtitles:
        if isinstance(subtitles[0], dict):
            return pd.Series({'channel_name': subtitles[0].get('name', None),
                              'channel_url': subtitles[0].get('url', None)})
    
    return pd.Series({'channel_name': None, 'channel_url': None})

# Sorts the data frame by week days (i.e. from Monday to Sunday)
def process_yearly_data(data, year):
    # Filter the DataFrame for the specified year
    df_year = data[data['year'] == year]
    
    # Sort the DataFrame by day and time in ascending order
    df_sorted = df_year.sort_values(by=['day_of_the_week', 'time_of_day'])

    # Define the order of days of the week
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # Convert 'day_of_week' to Categorical with the specified order
    df_sorted['day_of_the_week'] = pd.Categorical(df_sorted['day_of_the_week'], categories=day_order, ordered=True)

    # Count the number of observations per day of the week
    sorted_day = df_sorted.groupby(['year', 'day_of_the_week']).size().reset_index(name='No. watched videos')

    return sorted_day

# Sorts the data frame by hours of the day (i.e. from midnight 00:00 to 23:00)
def df_by_hour(data):
    # Make a copy of the input DataFrame
    data_copy = data.copy()

    # Set the day of the week values
    data_copy['day_of_the_week'] = data_copy['time'].dt.day_name()
    
    # Extract the hour component
    data_copy['hour'] = data_copy['time'].dt.hour

    # Extract the year component
    data_copy['year'] = data_copy['time'].dt.year

    # Count the number of observations for each hour
    watched_data = data_copy.groupby(['year', 'hour', 'time']).size().reset_index(name='no. watched')

    return watched_data