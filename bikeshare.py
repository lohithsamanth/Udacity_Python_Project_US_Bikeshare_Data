import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']
WEEKDAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


# call get_filter() functions to return city, month & day
def get_filters():
    city = get_city()
    month = get_month()
    day = get_day()

    print('-' * 40)
    return city, month, day


def get_city():
    """
    Asks user to specify a city
    Returns:
        (str) city - name of the city to analyze
    """

    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington).
    city_list = ['chicago', 'new york city', 'washington']
    while True:
        city = input('\nPlease select one of the following cities (chicago, new york city, washington)\n').lower()
        if (city in city_list):
            break
    return city


# TO DO: get user input for month (all, january, february, ... , june)
def get_month():
    """
    Asks user to specify a month
    Returns:
        (str) month - name of the month to filter by, or "all" to apply no month filter
    """
    while True:
        month = input("    Enter the month with January=1, June=6 or 'a' for all:  ")

        if month == 'a':
            month = 'all'
            break
        elif month in {'1', '2', '3', '4', '5', '6'}:
            # reassign the string name for the month
            month = MONTHS[int(month) - 1]
            break
        else:
            continue

    return month


# TO DO: get user input for day of week (all, monday, tuesday, ... sunday)

def get_day():
    """
    Asks user to specify a day to analyze.
    Returns:
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    while True:
        day = input("    Enter the day with Monday=1, Sunday=7 or 'a' for all:  ")

        if day == 'a':
            day = 'all'
            break
        elif day in {'1', '2', '3', '4', '5', '6', '7'}:
            # reassign the string name for the day
            day = WEEKDAYS[int(day) - 1]
            break
        else:
            continue

    return day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month, day of week & hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int

        month = MONTHS.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    month = MONTHS[df['month'].mode()[0] - 1].title()
    print('    Month:               ', month)
    # TO DO: display the most common day of week
    common_day = df['day_of_week'].mode()[0]  # day in df is 0-based
    print('    Day of the week:     ', common_day)
    # TO DO: display the most common start hour
    hour = df['hour'].mode()[0]
    print('    Start hour:          ', hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    start_station_trips = df['Start Station'].value_counts()[start_station]

    print('Start station:         ', start_station)
    print('Total trips from this station is: {}'.format(start_station_trips))
    print()
    # TO DO: display most commonly used end station
    end_station = df['End Station'].mode()[0]
    end_station_trips = df['End Station'].value_counts()[end_station]

    print('End station:            ', end_station)
    print('Total trips to this station is: {}'.format(end_station_trips))
    print()
    # TO DO: display most frequent combination of start station and end station trip
    result = df[['Start Station', 'End Station']].groupby(['Start Station', 'End Station']).size().nlargest(1)
    print('Most Frequent trip is:\n')
    print(result)
    print()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('    Total travel time:   ', total_travel_time, ' Seconds')
    print()
    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('    Mean travel time:    ', mean_travel_time, ' Seconds')
    print()
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    for i in range(len(user_types)):
        val = user_types[i]
        user_type = user_types.index[i]
        print('    {0:21}'.format((user_type + ':')), val)
    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        # Display counts of gender
        genders = df['Gender'].value_counts()
        for i in range(len(genders)):
            val = genders[i]
            gender = genders.index[i]
            print('    {0:21}'.format((gender + ':')), val)
    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        # Display earliest, most recent, and most common year of birth
        print('    Year of Birth...')
        print('        Earliest:        ', int(df['Birth Year'].min()))
        print('        Most recent:     ', int(df['Birth Year'].max()))
        print('        Most common:     ', int(df['Birth Year'].mode()))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def display_data(df):
    """
    Display 5 lines of raw data based on the user input. 
    Continue showing until user say no
    """
    show_rows = 5
    start = 0
    end = show_rows - 1    # use index values for rows

    
    while True:
        raw_data = input(' Would you like to see some raw data from the current dataset?     type(y or n):  ')
        if raw_data.lower() == 'y':

            print('\n    Displaying rows {} to {}:'.format(start + 1, end + 1))

            print('\n', df.iloc[start : end + 1])
            start += show_rows
            end += show_rows

            
            print('\n    Would you like to see the next {} rows?'.format(show_rows))
            continue
        else:
            break
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
