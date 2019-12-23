import time
import pandas as pd
import numpy as np
import calendar

#This project was made based on a template by Udacity
#those guys are the best!
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
    print('#'*80)
    print('# Hi There! I am Nihad,  \n #Let\'s explore some US bikeshare data!\n\n')
    print('#'*80)
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    out = False
    city = str(input("Which City would you like to check out? \n Chicago - New York City - Washington \n >>"))
    city= city.lower()
    while not out:
        if city not in ('chicago','new york city','washington'):
            print("Please make sure you spell the city as described. \n\n\n Restarting ...\n")
            city = str(input("Which City would you like to check out? \n Chicago - New York - Washington \n >>"))
            city= city.lower()
        else:
            out=True
    print("   You have chosen {}".format(city))

    # get user input for month (all, january, february, ... , june)
    out= False
    month = str(input("Which Month would you like? \n all, january, february, ... , june \n >>"))
    month = month.lower()
    while not out:
        if month.lower() not in ('all','january','february','march','april','may','june','july','august','september','october','november','december'):
            print("Please make sure you spell the month as described.")
            month = str(input("Which Month would you like? \n all, january, february, ... , december \n >>"))
            month = month.lower()
        else:
            out=True

    print("   You have chosen {}".format(month))

    # get user input for day of week (all, monday, tuesday, ... sunday)
    out= False
    day = str(input("Which day would you like? \n all, 0 for monday, 1 for tuesday, ..., 6 for sunday \n >>"))
    month = month.lower()
    while not out:
        if day.lower() not in ('all','0','1','2','3','4','5','6'):
            print("Please make sure you spell the day as described.")
            day = str(input("Which day would you like? \n all, 0 for monday, 1 for tuesday, ..., 6 for sunday \n >>"))
            month = month.lower()
        else:
            out=True
    print("   You have chosen {}".format(day))
    print('*'*40)
    print("End of inputs")

    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """
    print('*'*40)
    print("Starting the Filtering process")
    print('*'*40)

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] =pd.to_datetime(df['Start Time'], errors='raise')


    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    # filter by month if applicable

    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january','february','march','april','may','june','july','august','september','october','november','december']
        month_int = months.index(month)+1

        # filter by month to create the new dataframe
        df = df[(df['month']==month_int)]
        print("The number of items after filtering by month is : {}".format(df.size))
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df =df[df['day_of_week']==int(day)]
        print("The number of items after filtering by day is : {}".format(df.size))

    if df.isnull().values.any() :
        df = df.dropna(axis=0)
        print("The number of items after deleting NaNs is : {}".format(df.size))

    print("\nThe final number of items after filtering is : {}".format(df.size))
    print("\n#Returning the filtered Dataframe ...\n\n")
    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""
    print('*'*40)
    print('Calculating Time statistics...')
    print('*'*40)
    start_time = time.time()

    # display the most common month
    if month == 'all':
        mc_month= df['Start Time'].dt.month.value_counts().idxmax()
        print("The most popular month of travel is  {}".format(mc_month))

    # display the most common day of week
    if day == 'all':
        mc_dow= df['Start Time'].dt.weekday_name.value_counts().idxmax()
        print("The most popular day of travel is  {}".format(mc_dow))

    # display the most common start hour
    mc_hour= df['Start Time'].dt.hour.value_counts().idxmax()
    print("The most popular Hour of travel is  {} ".format(mc_hour))

    print("\n#This took %s seconds.\n\n" % (time.time() - start_time))

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('*'*40)
    print('Calculating The Most Popular Stations and Trip...')
    print('*'*40)
    start_time = time.time()

    # display most commonly used start station
    mc_sstation= df['Start Station'].value_counts().idxmax()
    print("The most popular start station is  \'{}\'".format(mc_sstation))

    # display most commonly used end station
    mc_estation= df['End Station'].value_counts().idxmax()
    print("The most popular end station is  \'{}\'".format(mc_estation))

    # display most frequent combination of start station and end station trip
    df_combination_stations= pd.DataFrame({'count' : df.groupby( [ 'Start Station','End Station'] ).size()}).reset_index()
    df_combination_stations= df_combination_stations.sort_values(by='count', axis=0, ascending=False, inplace=False, kind='quicksort', na_position='last')
    #print(df_combination_stations.head(5))
    print("The most popular combination of stations is  \'{}\' to \'{}\' with a count of: {} trips".format(df_combination_stations.iloc[0]['Start Station'], df_combination_stations.iloc[0]['End Station'],df_combination_stations.iloc[0]['count']))

    print("\n#This took %s seconds.\n\n" % (time.time() - start_time))


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('*'*40)
    print('Calculating Trip Duration')
    print('*'*40)
    start_time = time.time()
    df['Start Time'] =pd.to_datetime(df['Start Time'], errors='raise')
    df['End Time'] =pd.to_datetime(df['End Time'], errors='raise')

    df.rename(columns = {"End Time": "end_s", "Start Time":"start_s"}, inplace = True)

    # display total travel time
    df['trip_duration'] = df.apply(lambda row: row.end_s - row.start_s, axis=1)

    total = df['trip_duration'].sum()
    print("Total travel time is : {} h".format(total))
    # display mean travel time
    mean = df['trip_duration'].mean()
    print("Mean travel time is : {} h".format(mean))

    print("\n#This took %s seconds.\n\n" % (time.time() - start_time))


def user_stats(df, city):
    """Displays statistics on bikeshare users."""
    print('*'*40)
    print('Calculating User Stats')
    print('*'*40)
    start_time = time.time()

    # Display counts of user types

    # print value counts for each user type
    user_types = df['User Type'].value_counts()

    print("The user types in our data are :\n{}\n".format(user_types))

    if city != 'washington':
        # Display counts of gender
        gender_types = df['Gender'].value_counts()

        print("The gender types in our data are : \n {}\n".format(gender_types))

        # Display earliest, most recent, and most common year of birth
        year_max = df['Birth Year'].value_counts().idxmax()
        year_earliest = df['Birth Year'].value_counts().idxmax()


        print("The most common year of birth is : {}".format(year_max))
        print("The earliest year of birth is : {}".format(year_earliest))


    print("\n#This took %s seconds.\n \n" % (time.time() - start_time))
    print('*'*40)


def main():
    while True:

        city, month, day = get_filters()
        df = load_data(city, month, day)
        trip_duration_stats(df)
        t_stats= input('\nWould you like to see time stats? Enter y or n.\n')
        if t_stats.lower() != 'n':
            time_stats(df,month,day)

        s_stats= input('\nWould you like to see station stats? Enter y or n.\n')
        if s_stats.lower() != 'n':
            station_stats(df)

        u_stats= input('\nWould you like to see user stats? Enter y or n.\n')
        if u_stats.lower() != 'n':
            user_stats(df,city)

        raw_data =input('\nWould you like to see raw? Enter y or n.\n')
        current_row=4
        while raw_data.lower() != 'n':
            to_print_data= df[current_row-4:current_row]
            for i,line in to_print_data.iterrows():
                print("Start station : {}".format(line['Start Station']))
                print("End station : {}".format(line['End Station']))
                print("Trip duration : {}".format(line['trip_duration']))
                print("Day of the week : {}".format(line['day_of_week']))
                print("User type : {}".format(line['User Type']))
                if city !='washington':
                    print("Birth year : {}".format(line['Birth Year']))
                    print("Gender  : {}".format(line['Gender']))
                print('+'*80)
            current_row+=5
            raw_data =input('\nWould you like to see raw? Enter y or n.\n')


        restart = input('\nWould you like to restart? Enter y or n.\n')
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()
