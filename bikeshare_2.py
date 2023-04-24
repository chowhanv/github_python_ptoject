import time

import numpy as np
import pandas as pd

#dictonary of city and data files used

CITY_DATA = {
    "chicago": "chicago.csv",
    "new york city": "new_york_city.csv",
    "washington": "washington.csv",
}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let's explore some US bikeshare data!")
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input(
            "\nWhich city would you like to filter by - New York City, Chicago or Washington?\n"
        ).lower()
        if city not in ("new york city", "chicago", "washington"):
            print(
                "Invalid Input. Input must be: chicago, new york city, or washingtonTry again. Try Again"
            )
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input(
            "\nWhich month would you like to filter by - January, February, March, April, May, June or type 'all' if you do not have any preference?\n"
        ).lower()
        if month not in ("january", "february", "march", "april", "may", "june", "all"):
            print(
                "Invalid Input. Input must be: January, February, March, April, May, June or All. Try again."
            )
            continue
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input(
            "\nAre you looking for a particular day or all? If a day enter: Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or type 'all' if you do not have any preference.\n"
        ).lower()
        if day not in (
            "sunday",
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "all",
        ):
            print(
                "Invalid Input. Input must be: Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or All. Try again."
            )
            continue
        else:
            break

    print("-" * 40)
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
    df["Start Time"] = pd.to_datetime(df["Start Time"])

    # extract month and day of week from Start Time to create new columns
    df["month"] = df["Start Time"].dt.month
    df["day_of_week"] = df["Start Time"].dt.day_name()

    # filter by month if applicable
    if month != "all":
        # use the index of the months list to get the corresponding int
        months = ["january", "february", "march", "april", "may", "june"]
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df["month"] == month]

    # filter by day of week if applicable
    if day != "all":
        # filter by day of week to create the new dataframe
        df = df[df["day_of_week"] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()
    # df.reset_index(drop=True, inplace=True)
    # display the most common month
    common_month = df["month"].mode()[0]
    print("Most Common Month:", common_month)

    # display the most common day of week
    common_day = df["day_of_week"].mode()[0]
    print("Most Common day:", common_day)

    # display the most common start hour
    df["hour"] = df["Start Time"].dt.hour
    common_hour = df["hour"].mode()[0]
    print("Most Common Hour:", common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df["Start Station"].mode()[0]
    print("Most Common Start Station is: ", most_common_start_station)

    # display most commonly used end station
    most_common_end_station = df["End Station"].mode()[0]
    print("Most Common End Station is: ", most_common_end_station)

    # display most frequent combination of start station and end station trip
    combination_group = df.groupby(["Start Station", "End Station"])
    most_frequent_combination_station = (
        combination_group.size().sort_values(ascending=False).head(1)
    )
    print(
        "Most frequent combination of Start Station and End Station trip is: ",
        most_frequent_combination_station,
    )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    # display total travel time
    total_travel_time = df["Trip Duration"].sum()
    print("Total Travel Time is: ", round(total_travel_time, 2), " seconds")

    # display mean travel time
    mean_travel_time = df["Trip Duration"].mean()
    print("Mean Travel Time is: ", round(mean_travel_time, 2), " seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print("\nCalculating User Stats...\n")
    start_time = time.time()

    # Display counts of user types
    user_types = df["User Type"].value_counts()
    # print(user_types)
    print("User Types:\n", user_types)

    # Display counts of gender
    try:
        gender_types = df["Gender"].value_counts()
        print("\nGender Types:\n", gender_types)
    except KeyError:
        print("\nGender Types:\nNo data available for this month.")

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_year = df["Birth Year"].min()
        print("\nEarliest Year:", round(earliest_year))
    except KeyError:
        print("\nEarliest Year:\nNo data available for this month.")

    try:
        most_recent_year = df["Birth Year"].max()
        print("\nMost Recent Year:", round(most_recent_year))
    except KeyError:
        print("\nMost Recent Year:\nNo data available for this month.")

    try:
        most_common_year = df["Birth Year"].mode()[0]
        print("\nMost Common Year:", round(most_common_year))
    except KeyError:
        print("\nMost Common Year:\nNo data available for this month.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def display_raw_data(df):
    """Script to prompt the user whether they would like to see the raw data"""
    i = 0
    raw = input("\nWould you like to see the raw data?\n").lower()
    pd.set_option("display.max_columns", 200)

    while True:
        if raw == "no":
            break
        elif raw == "yes":
            print(
                df[i : i + 5]
            )  # TO DO: appropriately subset/slice your dataframe to display next five rows
            raw = input("\nWould you like to see the next 5 rows?\n").lower()
            i += 5
        else:
            raw = input(
                "\nYour input is invalid. Please enter only 'yes' or 'no'\n"
            ).lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        display_raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        while True:
            restart = input("\nWould you like to restart? Enter yes or no.\n").lower()
            if restart not in ("yes", "no"):
                print("Invalid Input. Input must be: Yes or No. Try Again")
                continue
            else:
                break
        if restart == "no":
            break


if __name__ == "__main__":
    main()