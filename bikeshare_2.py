import time
from calendar import month

import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

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
        city = str(input("Please enter the city (Chicago,new york,washington): ").lower())
        if city in CITY_DATA.keys():
            break
        print("Invalid city, Please enter a valid city name")

    # get user input for month (all, january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    while True:
        month = str(input("Enter a month (all, january, february, ... , june): ").lower())
        if month == 'all' or month in months:
            break
        print("Invalid month, Please enter a valid month name")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while True:
        day = str(input("Enter a day of the week(all, monday, tuesday, ... sunday): ").lower())
        if day == 'all' or day in days:
            break
        print("Invalid day, Please enter a valid day")


    print('-'*40)
    return city, month, day


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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = (df['Start Time']).dt.month
    df['day'] = (df['Start Time']).dt.day_name().str.lower()

    #filter by month
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month_num = months.index(month)+1
        while month_num not in df['month'].unique():
            print(f"No data available for the month {month}, Please enter another month")
            month = input("Enter a month (all, january, february, ... , june): ").lower()
            month_num = months.index(month) + 1
        df = df[df['month'] == month_num]

    #filter by day
    if day != 'all':
        while day not in df['day'].unique():
            print(f"No data available for the day {day}, Please enter another day")
            day = input("Enter a day of the week(all, monday, tuesday, ... sunday):  ").lower()
        df = df[df['day'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    if df.empty:
        print("No data available to calculate")
        return

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if 'month' in df.columns:
        try:
            popular_month = df['month'].mode()[0]
            print('Most Popular Month:', popular_month)
        except IndexError:
            print("No data available")
    else:
        print("month column not found in df")

    # display the most common day of week
    if 'day' in df.columns:
        try:
            popular_day_of_week = df['day'].mode()[0]
            print('Most Popular day of the week:', popular_day_of_week)
        except IndexError:
            print("No data available")
    else:
        print("date column not found in df")

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular start hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Popular start Station:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Popular end station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    """ combine start and end station with zip to create a combination station and count each combination and use idmax to get max tuple,count max """
    df['Station Combo'] = list(zip(df['Start Station'], df['End Station']))
    combo_count = df['Station Combo'].value_counts()

    popular_combination = combo_count.idxmax()
    count = combo_count.max()
    print(f"The most frequent combination is from {popular_combination[0]} tp {popular_combination[1]} with {count} trips.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_trip = df['Trip Duration'].sum()
    print(f"The total travel time: {total_trip} seconds.")

    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    print(f"Mean travel time: {mean_time:.2f} seconds.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    if 'User Type' not in df.columns:
        print("User type not available in this city")
    else:
        user_count = df['User Type'].value_counts()
        print(f"The number of user type: {user_count}")

    # Display counts of gender
    if 'Gender' not in df.columns:
        print("Gender is not available in this city")
    else:
        gender_count = df['Gender'].value_counts()
        print(f"The gender counts are: {gender_count}")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' not in df.columns:
        print("Birth year is not available in the city")
    else:
        most_comman_year = df['Birth Year'].mode()[0]
        print(f"The most common birth year is: {most_comman_year}")

        earliest_birth = df['Birth Year'].min()
        print(f"The earliest birth year is: {earliest_birth}")

        most_recent = df['Birth Year'].max()
        print(f"The most recent birth year is: {most_recent}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
