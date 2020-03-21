import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
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
    city, month, day = ('none','none','none')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while city not in ['chicago', 'new york city', 'washington']:
        city = input("Enter city (chicago, new york city or washington): ").lower()

    # get user input for month (all, january, february, ... , june)
    while month not in ['all','january', 'february', 'march', 'april', 'may', 'june']:
        month = input("Enter month (e.g. january, february,..., or june) or type all for no month filter: ").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while day not in ['all','monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
        day = input("Enter day of week or type all for no day filter: ").lower()

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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['start_hour'] = df['Start Time'].dt.hour
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
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
    month = df['month'].mode()[0]
    print("Most common month: {}".format(month))

    # display the most common day of week
    day_of_week = df['day_of_week'].mode()[0]
    print("Most common day of week: {}".format(day_of_week))

    # display the most common start hour
    start_hour = df['start_hour'].mode()[0]
    print("Most common start hour: {}".format(start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print("Most common start station: {}".format(start_station))

    # display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print("Most common end station: {}".format(end_station))

    # display most frequent combination of start station and end station trip
    combo = (df['Start Station'] + ' to ' + df['End Station']).mode()[0]
    print("Most common combination of start and end station: {}".format(combo))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    tot_dur = df['Trip Duration'].sum()
    print("Total travel time: {}".format(tot_dur))

    # display mean travel time
    avg_dur = df['Trip Duration'].mean()
    print("Average travel time: {}".format(avg_dur))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Count of user types:")
    print(df["User Type"].value_counts())

    # Display counts of gender
    if 'Gender' in df.columns:
        print("Count of gender:")
        print(df["Gender"].value_counts())
    else: 
        print("Dataset has no Gender info")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest = df['Birth Year'].min()
        recent = df['Birth Year'].max()
        common = df['Birth Year'].mode()[0]
        print("Earliest birth year: {}, most recent: {}, most common: {}.".format(earliest,recent,common))
    else: 
        print("Dataset has no Birth Year info")
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    ans = input("Do you want to see raw data? Type y for yes otherwise just hit enter to skip: ").lower()
    i=0
    while ans == 'y':
        if i+5<= df.size:
            print("Displaying lines {} to {}:".format(i,i+4))
            print(df.iloc[i:i+5,:])
            ans = input("Do you want to see 5 more lines. Type y for yes otherwise just hit enter to skip: ").lower()
            i+= 5
        elif (df.size - i) >0 and (df.size - i) < 5:
            print("Displaying lines {} to {}:".format(i,i+4))
            print(df.iloc[i:,:])
            ans = input("Do you want to see 5 more lines. Type y for yes otherwise just hit enter to skip: ").lower()
            i+= 5
        else:
            print("Reached end of dataset")
            ans = 'n'

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