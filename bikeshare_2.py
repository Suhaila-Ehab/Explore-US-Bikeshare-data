import time
import pandas as pd
import numpy as np
import calendar

CITY_DATA = { 'ch': 'chicago.csv',
              'ny': 'new_york_city.csv',
              'w': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city_abrev= ['ch', 'ny', 'w']
        city= input('Choose a city: \n Please type (ch) for Chicago \n Please type (ny) for New York City \n Please type (w) for Washington \n').lower()
        if city not in city_abrev:
            print('Invalid City, please try again')
        else:
            break
    # get user input for month (all, january, february, ... , june)
    while True:
        months= ['jan', 'feb', 'mar', 'apr', 'may','jun', 'all'] 
        month= input('Choose a month:\n Jan \n Feb \n Mar \n Apr \n Jun \n all \n').lower()
        if month not in months:
            print ('Invalid month, please try again')
        else:
            break
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        days = ["saturday", "sunday", "monday", "tuesday", "wednesday" , "thursday", "friday","all"]
        day= input('Choose a specific weekday: \n Saturday \n Sunday \n Monday \n Tuesday \n Wednesday \n Thursday\n Friday\n all\n').lower()
        if day not in days:
            print('Invalid weekday, please try again')
        else:
            break
        print('-'*40)
    return city , month, day

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

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun']
        month = months.index(month) + 1
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

    # display the most common month
    most_common_month= calendar.month_abbr[df['month'].mode().loc[0]]
    print('Most common month of travel is {}'.format(most_common_month))

    # display the most common day of week
    most_common_day= df['day_of_week'].mode().loc[0]
    print('Most common day of the week for travel is {}'.format(most_common_day))

    # display the most common start hour
    most_common_hour= df['Start Time'].dt.hour.mode().loc[0]
    print('Most common hour for travel is {}'.format(most_common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_st= df['Start Station'].mode().loc[0]
    print('Most common start station is {}'.format(most_common_start_st))

    # display most commonly used end station
    most_common_end_st= df['End Station'].mode().loc[0]
    print('Most common end station is {}'.format(most_common_end_st))

    # display most frequent combination of start station and end station trip
    most_common_comb= df[['Start Station','End Station']].mode().loc[0]
    print('Most frequent combination of start station and end station trip is {}'.format(most_common_comb))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time= df['Trip Duration'].sum()
    print('Total travel time is {} hours'.format(total_travel_time/ 3600))


    # display mean travel time
    mean_travel_duration= df['Trip Duration'].mean()
    print('Mean travel duration is {} minutes'.format(mean_travel_duration/60))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types= df['User Type'].value_counts()
    print('User numbers filtered by type: {}'.format(user_types))
    # Display counts of gender
    try:
        counts_of_gender= df['Gender'].value_counts()
        print('User numbers filtered by gender: {}'.format(counts_of_gender))
    except KeyError:
        print('Washington holds no data for gender')
    # Display earliest, most recent, and most common year of birth
    try:
        earliest_yob= int(df['Birth Year'].min())
        latest_yob= int(df['Birth Year'].max())
        most_common_yob= int(df['Birth Year'].mode().loc[0])
        print('Our youngest users were born in: {}'.format(earliest_yob))
        print('Our oldest users were born in: {}'.format(latest_yob))
        print('Most common year of birth: {}'.format(most_common_yob))
    except KeyError:
        print('Washington holds no data for birth year')



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    show_data= input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
    start_loc = 0
    while(show_data=='yes'):
        print(df.iloc[start_loc:start_loc+5])
        start_loc +=5
        show_data= input('would you like to view another 5 rows? Enter yes or no\n').lower()

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
