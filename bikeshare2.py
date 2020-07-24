# run -pip install bullet- to instal bullet

from bullet import Bullet
from bullet import colors
import time
import pandas as pd
import numpy as np


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print ('Hello! My Name is Jason. Let\'s explore some US bikeshare data!')
    cli = Bullet(
            prompt = "\nPlease select a city [move 👉 cursor with arrow keys]",
            choices = ["chicago", "new york city", "washington"],
            indent = 0,
            align = 5,
            margin = 2,
            bullet = "👉",
            bullet_color=colors.bright(colors.foreground["cyan"]),
            word_color=colors.bright(colors.foreground["red"]),
            word_on_switch=colors.bright(colors.foreground["blue"]),
            background_color=colors.background["black"],
            background_on_switch=colors.background["black"],
            pad_right = 5
        )
    result = cli.launch()
    city = result
    print("You chose:", result)
    cli = Bullet(
            prompt = "\nPlease select month name(Only January to June or all [move 👉 cursor with arrow keys]",
            choices = ["all", "january", "february", "march", "april", "may", "june"],
            indent = 0,
            align = 5,
            margin = 2,
            bullet = "👉",
            bullet_color=colors.bright(colors.foreground["cyan"]),
            word_color=colors.bright(colors.foreground["red"]),
            word_on_switch=colors.bright(colors.foreground["blue"]),
            background_color=colors.background["black"],
            background_on_switch=colors.background["black"],
            pad_right = 5
        )
    result = cli.launch()
    month = result
    print("You chose:", result)
    cli = Bullet(
            prompt = "\nPlease select day of week or all [move 👉 cursor with arrow keys]",
            choices = ["all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"],
            indent = 0,
            align = 5,
            margin = 2,
            bullet = "👉",
            bullet_color=colors.bright(colors.foreground["cyan"]),
            word_color=colors.bright(colors.foreground["red"]),
            word_on_switch=colors.bright(colors.foreground["blue"]),
            background_color=colors.background["black"],
            background_on_switch=colors.background["black"],
            pad_right = 5
        )
    result = cli.launch()
    day = result
    print("You chose:", result)
    return (city, month, day)

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
    df = pd.read_csv("{}.csv".format(city.replace(" ","_")))

    # Convert the Start and End Time columns to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].apply(lambda x: x.month)
    df['day_of_week'] = df['Start Time'].apply(lambda x: x.strftime('%A').lower())


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df.loc[df['month'] == month,:]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df.loc[df['day_of_week'] == day,:]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Popular times of travel...\n')
    start_time = time.time()

    # display the most common month
    print("The most common month is: {}".format(
        str(df['month'].mode().values[0]))
    )

    # display the most common day of week
    print("The most common day of the week: {}".format(
        str(df['day_of_week'].mode().values[0]))
    )

    # display the most common start hour
    df['start_hour'] = df['Start Time'].dt.hour
    print("The most common start hour: {}".format(
        str(df['start_hour'].mode().values[0]))
    )


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most common start station is: {} ".format(
        df['Start Station'].mode().values[0])
    )

    # display most commonly used end station
    print("The most common end station is: {}".format(
        df['End Station'].mode().values[0])
    )

    # display most frequent combination of start station and end station trip
    df['routes'] = df['Start Station']+ " " + df['End Station']
    print("The most common start and end station combo is: {}".format(
        df['routes'].mode().values[0])
    )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    df['duration'] = df['End Time'] - df['Start Time']

    # display total travel time
    print("The total travel time is: {}".format(
        str(df['duration'].sum()))
    )

    # display mean travel time
    print("The mean travel time is: {}".format(
        str(df['duration'].mean()))
    )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User info...\n')
    start_time = time.time()

    # Display counts of user types
    print("Here are the counts of various user types:")
    print(df['User Type'].value_counts())

    if city != 'washington':
        # Display counts of gender
        print("Here are the counts of gender:")
        print(df['Gender'].value_counts())


        # Display earliest, most recent, and most common year of birth
        print("The earliest birth year is: {}".format(
            str(int(df['Birth Year'].min())))
        )
        print("The latest birth year is: {}".format(
            str(int(df['Birth Year'].max())))
        )
        print("The most common birth year is: {}".format(
            str(int(df['Birth Year'].mode().values[0])))
        )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    """
    Display contents of the CSV file to the display as requested by
    the user.
    """

    start_loc = 0
    end_loc = 5

    display_active = input('\nDo you want to see the raw data?:Enter yes or no\n').lower()

    if display_active == 'yes':
        while end_loc <= df.shape[0] - 1:

            print(df.iloc[start_loc:end_loc,:])
            start_loc += 5
            end_loc += 5

            end_display = input('\nDo you wish to continue?:Enter yes or no\n').lower()
            if end_display == 'no':
                break

def main():

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data(df)

        restart = input('\nWould you like to restart?:Enter yes or no\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
