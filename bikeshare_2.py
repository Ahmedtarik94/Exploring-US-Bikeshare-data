import time
import numpy as np
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

#Creating a list of cities, months and weekdays to validate user input
cities = ['chicago','new york city','washington']

months = ["january","february","march","april","may","june","all"]

weekdays = ["sunday","monday","tuesday","wednesday","thursday","friday","saturday","all"]

#Getting input from users.
def get_filters():
    print('Hello! Let\'s explore some US bikeshare data!')

    while True:
        try:
            city = input("Which city would you like to see data from? Chicago, New york city, Washignton?\n# ").lower()
            if city in cities:
                break
            else:
                print(city, "does not exist please enter a valid city name")
                continue
        except ValueError:
            Print("Please enter a valid city name")
            continue

    while True:
        try:
            month = input("\n\nWhich month would you like to see data from? all, january, february, march, april, may, june\n# ").lower()
            if month in months:
                break
            else:
                print("\n Sorry this month does not exist in my database, please enter a another month.")
        except ValueError:
            Print("Please enter a valid month")

    while True:
        try:
            day = input("\n\nWhich day would you like to see data from? all, monday, tuesday, wednsday ...etc\n# ").lower()
            if day in weekdays:
                break
        except ValueError:
            print("Please enter a valid day of the week")

    print('='*40)
    return city,month,day

def load_data(city,month,day):
    #loading data into dataframe.
    df = pd.read_csv(CITY_DATA[city])
    #Coverting start time column to datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    #Extracting columns of month , day and hour from Start Time datetime format
    df['month'] = df['Start Time'].dt.month
    df['days'] = df['Start Time'].dt.dayofweek
    df['hour'] = df ['Start Time'].dt.hour

    # Applying filter by month
    if month != 'all':
        month = months.index(month) + 1
        if month != 0:
            df = df[df['month'] ==  month]
        else:
            print("Sorry this month does not exist in my database\n")

    #Appluing filter by day.
    if day != 'all':
        day = weekdays.index(day) + 1
        if day != 0:
            df = df[df['days'] == day]
        else:
            print("Sorry this day does not exist in my database\n")

    return df


def timestats(df,month,day):
    """Calculating travel month , day and hour for user input"""

    print("\nCalculating The Most Frequent time of travel....\n")
    start_time = time.time()

    #Validating month filter
    #If user selected a specific month, it should calculate common day and hour only for this month
    if ((month != 'all') and (day == 'all')):
        print("Calculating most common travel day and hour of month: ", month.title())

        #Handling months that do not exist.
        try:
            popular_day = df['days'].mode()[0]
            print("\nMost Common Travel Day is: ",weekdays[popular_day -1].title())
            popular_hour = df['hour'].mode()[0]
            print("\nMost Common Travel Hour is: ",popular_hour, " hour(s)")

        except:
            print("\nSorry this month does not exist in my database")
    #Validating month and day filter
    elif ((month != 'all') and (day != 'all')):

        print("Calculating most common travel hour for day {} in month {}\n".format(day.title(),month.title()))
        #If user selected a specific day in a specific month, it should calculate common hour only.
        try:
            popular_hour = df['hour'].mode()[0]
            print("\nMost Common Travel Hour is: ",popular_hour, " hour(s)")
        except:
            print("Sorry this month or day does not exist in my database")

    #Validating day filter
    elif ((month == 'all') and (day != 'all')):
        print("Calculating most common travel month and hour for day: ", day)

    #Calculating most common month for this day and handling days that do not exist.
        try:
            popular_month = df['month'].mode()[0]
            print("\nMost Common Travel Month is: ",months[popular_month -1].title())

            popular_hour = df['hour'].mode()[0]
            print("\nMost Common Travel Hour is: ",popular_hour," hour(s)")

        except:
            print("Sorry this day does not exist in my database")

    #If no filters used, it should calculate the common month, day and hour.
    else:
        popular_month = df['month'].mode()[0]
        print("\nMost Common Travel Month is: ",months[popular_month -1].title())

        popular_day = df['days'].mode()[0]
        print("\nMost Common Travel Day is: ",weekdays[popular_day -1].title())

        popular_hour = df['hour'].mode()[0]
        print("\nMost Common Travel Hour is: ",popular_hour, " hour(s)")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def stationstats(df):
    """Calculating station statistics for applied filters"""

    print("\nCalculating The Most Frequest Stations and Trips....\n")
    start_time = time.time()
    try:
        popular_startstation = df['Start Station'].mode()[0]
        print("Most Common Start Station is: ",popular_startstation)

        popular_endstation = df['End Station'].mode()[0]
        print("\nMost Common End Station is: ",popular_endstation)

        """Groupby does not have mode() option so I used size() to get
        the number of elements rows x columns in the dataframe then sorted values
        in a descending manner then head(1) should be the most common value """

        trip = df.groupby(['Start Station','End Station'])
        popular_trip = trip.size().sort_values(ascending=False).head(1)
        print("\nMost Common Trip is:\n", popular_trip)

    except:
        print("Sorry this day or month does not exist in my database")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """ Calulcating total and average trip duration for user inputs"""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    try:
        print("Total Travel time is: ", df['Trip Duration'].sum().round(3), " seconds")
        print("\nAverage Travel time is: ", round(df['Trip Duration'].mean(),3) ," seconds")
    except:
        print("Sorry this day or month does not exist in my database")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df,city):

    """Calulating Gender and Birth Year statistics for user input"""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Washington does not have gender or birth year information, checking if city is washington...
    if city == "washington":
        print("\nSorry gender information is not available for washington\n")
    else:
        try:
            print("\nUser Gender\n", df['Gender'].value_counts())
            print("\nEarliest Year Of Birth: ", int(df['Birth Year'].max()))
            print("\nMost Recent Year Of Birth: ", int(df['Birth Year'].mean()))
            print("\nMost Common Year Of Birth: ", int(df['Birth Year'].mode()[0]))
        except:
            print("Sorry this day or month does not exist in my database")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def show_raw_data(df):
    """Displaying raw data upon user request, data is displayed in 5 rows
    until the user says no or end of dataframe reached"""

    #Extracting number of rows in iterator n
    n = df.shape[0]
    i=0
    #Iterating over the number of rows in the dataframe
    while i <= n:
        display_data = input("Would you like to see the raw data? yes/no\n# ")
        if display_data == 'yes':
            print(df[i:i+5])
            i+=5
        elif display_data == 'no':
            break
        else:
            #Handling invalid user input
            print("Invalid Input! Please enter yes or no")
            continue

def restart_program():

    while True:
        restart = input("Would you like to restart the program? yes/no\n# ").lower()
        if restart.lower() == 'no':
            break
        elif restart.lower() == 'yes':
            main()
        else:
            print("Invalid Input, please enter yes or no\n")

def main():

    city, month, day = get_filters()
    df = load_data(city,month,day)

    timestats(df,month,day)
    stationstats(df)
    trip_duration_stats(df)
    user_stats(df,city)
    show_raw_data(df)
    restart_program()


if __name__ == "__main__":
    main()
