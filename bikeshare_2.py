import time
import pandas as pd
import numpy as np
import calendar

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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('\nWould you like to see data for Chicago, New York, or Washington?\n')
        if city.lower() not in 'chicago new york washington':
            print("Sorry, I didn't understand that. Please enter the city name again.")
            continue
        else:
            break

    if 'chi' in city.lower():
        city = 'chicago'
    elif 'was' in city.lower():
        city = 'washington'
    elif 'new' in city.lower():
        city = 'new york city'

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('\nWould you like to filter by month (January thru June)? Enter the month name or \'all\'.\n')
        #this will make sure the month input is valid
        monlist = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
        if month.lower() not in monlist:
            print('Sorry, I didn\'t understand that. Please enter the month filter again.')
        else:
            break
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('\nWould you like to filter by day of the week? Enter day or \'all\'.\n')
        daylist = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']
        if day.lower() not in daylist:
            print('Sorry, I didn\'t understand that. Please enter the day filter again.')
        else:
            break
    print('\nTHANKS! \nYou have selected {} for the city; and {} and {} for the month and day filters.'.format(city.title(), month.title(), day.title()))

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
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    # filter by month if applicable
    if month.lower() != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month.lower()) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    # filter by day of week if applicable
    if day.lower() != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    #keeping this here to check on the data
    if False:    
        print(df.head(n=5))
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month- need to convert month back to name
    if df['month'].nunique() > 1:
        pop_month = df['month'].mode()[0]
        pop_month = calendar.month_name[pop_month]
        print('Most Popular Month:', pop_month)

    # display the most common day of week
    if df['day_of_week'].nunique() > 1:
        pop_weekday = df['day_of_week'].mode()[0]
        print('Most Popular Day of Week:', pop_weekday)

    # extract hour from the Start Time column to its own column -- month and weekday have columns
    df['hour'] = df['Start Time'].dt.hour
    # display the most popular hour
    pop_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', pop_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    pop_start = df['Start Station'].mode()[0]
    print('Most popular point of embarcation:', pop_start)

    # display most commonly used end station
    pop_end = df['End Station'].mode()[0]
    print('Most popular destination:', pop_end)

    # display most frequent combination of start station and end station trip
    df['combination'] = df['Start Station'] + ' to ' + df['End Station']
    pop_combination = df['combination'].mode()[0]
    print('Most frequent trip:', pop_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df['Trip Duration'].sum()/3600
    print('Total duration of all trips was {} hours.'.format(round(total_duration, 2)))
    # display mean travel time
    mean_duration = df['Trip Duration'].mean()
    m, s = divmod(mean_duration, 60)
    print('The average trip lasted {} minutes and {} seconds.'.format(int(m), int(s)))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_count = df['User Type'].value_counts()
    print('User types break down as follows:\n', user_type_count, '\n')
    # Display counts of gender and DoB if those columns exist.
    if 'Gender' in df.head(n=1):
        gender_count = df['Gender'].value_counts()
        print('User gender breaks down as follows:\n', gender_count, '\n')
        # Display earliest, most recent, and most common year of birth
        dob_earliest = df['Birth Year'].min()
        dob_recent = df['Birth Year'].max()
        dob_mode = df['Birth Year'].mode()[0]
        print('\nThe oldest rider was born in {}. (If that looks too old it could be a data error...)'.format(int(dob_earliest)),
                '\nThe youngest rider was born in {}.'.format(int(dob_recent)),
                '\nThe most common birth year for riders was {}.'.format(int(dob_mode)))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    '''Displays five lines of data if the user specifies that they would like to.
    After displaying five lines, ask the user if they would like to see five more,
    continuing asking until they say stop.

    Args:
        dataframe
    Returns:
        5 rows of data
    '''
    
    n = 5
    #display = input('\nWould you like to view individual trip data?\n'
        #'Type \'yes\' or \'no\'.\n')
    while True: 
        display = input('\nWould you like to view individual trip data?\n'
            'Type \'yes\' or \'no\'.\n')
        if display.lower() == 'yes':
            print('\nYou said yes. Here\'s that data!\n')
            print(df.iloc[(n-5):n])
            n += 5
        elif display.lower() == 'no':
            print('\nYou said no. Thanks anyways!')
            break            
        else:
            print('\nDidn\'t catch that. Try again.')
   

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
