import time
import pandas as pd
import os.path
import calendar
from statistics import mode
import numpy as np

#dictionary to hold csv filenames per city
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

total_row_count = int(0)

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    def get_month():
        """
        gets user input for month (all, january, february, ... , june)
        
        Returns:
            (str) month - name of the month in lowercase
        """
        month = input("Please enter a month (all, january, february, ... , june)").lower()
        months = ['all','january','february','march','april','may','june']
        #This loops manages any typos - month names should be entered in full
        while months.count(month.lower()) == 0:
            month = input("Please make sure the month is valid (all, january, february, ... , june)").lower()
        return month
    
    def get_day():
        """
        gets user input for day of the week (all, monday, tuesday, ... sunday)
        
        Returns:
            (str) day of the week - name of the day in lowercase
        """
        day = input("Please enter a day name (all, monday, tuesday, ... sunday)").lower()
        day_names = ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']
        #This loop manages any typos - day of the week should be entered in full
        while day_names.count(day) == 0:
            day = input("Please make sure the day name is valid (all,monday,tuesday,wednesday,thursday,friday,saturday,sunday)").lower()
        return day
    
    #welcome note
    print('Hello! Let\'s explore some US bikeshare data!')
    print('\nNOTE FOR ADMINS: Please make sure the csv files are in the same folder as the Python script file.')
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("\nPlease choose a city to explore its data. Chicago, New York City or Washington?\n").lower()
    cities = ['chicago', 'new york city', 'washington']
    print_case = 0
    #this loop manages any typos or incorrect input for city
    while cities.count(city) == 0:
        if print_case == 0:
            city = input("Please make sure the city is one of Chicago, New York City or Washington?\n").lower()
            print_case += 1
        else:
            city = input("Typo perhaps? Chicago, New York City or Washington?\n").lower()
    print('\nThank you! You have selected',city.title())
    
    #user interaction to provide filters for data set
    print('\nYou can see the analysis on all the data or on a set narrowed down by month and/or day of the week.')
    print('\nPlease type ALL for the analysis to start with no filters. Otherwise, type MONTHS to filter by month or DAYS to filter by day of the week.')
    input_filter = input('Please note that invalid inputs will be dismissed :')
    input_filter = input_filter.lower()
    
    #default values for month and day filters are set to all
    month = 'all'
    day = 'all'
    
    if input_filter == 'all':
        pass
    else:
        if(input_filter =='months' or input_filter == 'month'):
            # get user input for month (all, january, february, ... , june)
            month = get_month()
            input_filter = input('Would you also like to filter by day of the week? Y/N\n').lower()
            if (input_filter == 'y' or input_filter == 'yes' ):
                day = get_day()
        elif(input_filter == 'days' or input_filter == 'day'):
            # get user input for day of week (all, monday, tuesday, ... sunday)
            day = get_day()
            input_filter = input('Would you also like to filter by month? Y/N\n').lower()
            if (input_filter == 'y' or input_filter == 'yes' ):
                month = get_month()
        else:
            #in case the user input is not valid, it will be assumed that there are no filters chosen
            print('Sorry! Your input was not valid. The analysis is now running for all months')
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
    
    #overview of the selected filters
    print('The report filters are') 
    print('City:',city.title())
    print('Month:',month.title())
    print('Day:',day.title())
    
    #set the file path to the working directory. Hence why the printed note to admins at the start
    cwd = os.path.dirname(__file__)
    file_name = CITY_DATA.get(city)
    full_path = os.path.join(cwd, str(file_name))
   
    df = pd.read_csv(full_path)
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df.loc[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df.loc[df['day_of_week'] == day.title()]
    
    #total row count is calculated after applying all the input filters
    global total_row_count
    total_row_count = df['Start Time'].count()
    print('\nTotal number of rows after applying provided filters:',total_row_count)
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # display the most common month
    print('The most common month:', calendar.month_name[df['month'].value_counts().idxmax()])

    # display the most common day of week
    print('The most common day of the week:', df['day_of_week'].value_counts().idxmax())
    
    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print('The most common start hour (24-hour):', df['hour'].value_counts().idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('Calculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most common start station: ', df['Start Station'].value_counts().idxmax())

    # display most commonly used end station
    print('The most common end station: ', df['End Station'].value_counts().idxmax())

    # display most frequent combination of start station and end station trip
    # combination of str from start station and end station are combined into a list for calculating the most common combination using mode
    combination_list = np.array([])
    combination_list = (df['Start Station'] + ' > ' + df['End Station']).to_numpy()
    print('The most most frequent combination of start station and end station trip: ', mode(combination_list))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('The total travel time:', df['Trip Duration'].sum(),'hours')

    # display mean travel time
    print('The mean travel time:', int(df['Trip Duration'].mean()), 'hours')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """
    Displays statistics on bikeshare users (user type, gender and birth year).
    This function manages errors in case any of the additional information columns are missing.
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    try:
        # Display counts rows with no data on User Type
        print('There are', df['User Type'].isnull().sum(), 'rows with no data on user type')
        # Display counts of user types
        print(df['User Type'].value_counts())
        
    except:
        print('There are no data on User Type in this data set')
    
    try:
        # Display counts rows with no data on Gender
        print('\nThere are', df['Gender'].isnull().sum(), 'rows with no data on gender')
        # Display counts of gender
        print(df['Gender'].value_counts())
    except:
        print('There are no data on Gender in this data set')
        
    try:    
        # Display counts rows with no data on Birth Year
        print('\nThere are', df['Birth Year'].isnull().sum(), 'rows with no data on user birth year')
        # Display earliest, most recent, and most common year of birth
        print('The earliest birth year:', int(df['Birth Year'].min()))
        print('The most recent birth year:', int(df['Birth Year'].max()))
        print('The most common birth year:', int(df['Birth Year'].value_counts().idxmax()))
    except:
        print('There are no data on Birth Year in this data set')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    """ Displays 5 rows at a time based on user request."""

    view_data = input("Would you like to view first 5 rows of individual trip data? Y/N\n").lower()
    start_loc = 5
    df.rename(columns={'Unnamed: 0':'Record ID'}, inplace=True)
    
    while (view_data == 'y' or view_data == 'yes'):
        if(start_loc<total_row_count):
            #print(start_loc)
            print(df.iloc[start_loc-5:start_loc])
            start_loc += 5
            view_data = input("Do you wish view the next 5 rows? Y/N\n ").lower()
        elif(start_loc - 5 < total_row_count):
            #Handles the last few rows which are less than 5
            print('There are only ', total_row_count - (start_loc - 5), ' rows left.')
            view_data = input('Would you like to view them? Y/N\n').lower()
            if(view_data == 'y' or view_data == 'yes'):
                print(df.iloc[start_loc-5:(total_row_count)])

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
