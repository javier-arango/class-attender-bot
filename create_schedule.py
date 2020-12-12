# Import libraries
import sqlite3
from os import path
import re


# Create schedule database
def create_schedule_DB():
    # Database connection
    conn = sqlite3.connect('schedule.db')

    # Database cursor
    c = conn.cursor()

    # Create table
    c.execute('''CREATE TABLE schedule (classCode text, classDay text, classStart text, classFinish text)''')

    # Save (commit) the changes
    conn.commit()

    # Close connection
    conn.close()


# Add data to the schedule database
def add_data_to_schedule_DB(class_code_, week_day_, class_start_, class_finish_):
    # Database connection
    conn = sqlite3.connect('schedule.db')
    c = conn.cursor()  # Database cursor

    # Insert a row of data
    c.execute("INSERT INTO schedule VALUES ('%s','%s','%s','%s')" % (class_code_, week_day_, class_start_, class_finish_))

    conn.commit()  # Save (commit) the changes
    conn.close()  # Close connection

    # Print feedback
    print("Class added to database")


# Get schedule
def get_and_add_schedule():
    # Check if schedule database is already created
    if not(path.exists('schedule.db')):
        create_schedule_DB() # Create database and table

    # Get number of courses
    while True:
        try:
            # Get number of courses
            number_of_courses = int(input('How many courses are you taking this semester ?\nPlease enter a number: '))
            break

        except:
            print('That is not a valid option! Please try again but this time only enter a number.\n')

    # Numbers indicators
    indicators = ['st', 'nd', 'rd']

    # Get info for every class
    for i in range(number_of_courses):
        try:
            # Get every class code
            class_code = input('\nPlease enter your {}{} class code exactly like it appear in BlackBoard: (MAC2313-2207-4921/PHY2049-2207-6214) '.format(i+1, indicators[i]))

            # Get class hours and days and add it to the database
            get_class_hours_and_days(class_code)

        except:
            # Get every class code
            class_code = input('\nPlease enter your {}th class code exactly like it appear in BlackBoard: (MAC2313-2207-4921/PHY2049-2207-6214) '.format(i+1))

            # Get class hours and days and add it to the database
            get_class_hours_and_days(class_code)


# Get class hours
def get_class_hours_and_days(class_codes):
    # Global variable
    week_day_list = []

    # Get number of days (days that you going to take the class)
    while True:
        try:
            # Get number of days
            number_of_days = int(input('How many days are you going to take this class ?\nPlease enter a number: '))
            break

        except:
            print('That is not a valid option! Please try again but this time only enter a number.\n')

    indicators = ['st', 'nd', 'rd']

    for i in range(number_of_days):
        try:
            # Get the days of the week for that class
            days = input('Enter {}{} day that you are going to take this course: (Monday/Tuesday/Wednesday..etc) '.format(i+1, indicators[i]))

            # Check week day input
            while not(validate_week_days_input(days.strip())):
                print("\nInvalid input. Please try again")
                days = input('Enter {}{} day that you are going to take this course: (Monday/Tuesday/Wednesday..etc) '.format(i+1, indicators[i]))

            # Add the days to the list
            week_day_list.append(days)

        except:
            # Get the days of the week for that class
            days = input('Enter {}th day that you are going to take this course: (Monday/Tuesday/Wednesday..etc) '.format(i+1))

            # Check week day input
            while not (validate_week_days_input(days.strip())):
                print("\nInvalid input. Please try again")
                days = input('Enter {}th day that you are going to take this course: (Monday/Tuesday/Wednesday..etc) '.format(i+1))

            # Add the days to the list
            week_day_list.append(days)

    # Add the week days list to just one string
    week_day = ', '.join(week_day_list)

    # Get the class starting time
    class_start = input('Enter class start time in 24 hour format: (HH:MM) ')

    # Check time input
    while not (validate_time_input(class_start)):
        print("\nInvalid input. Please try again")
        class_start = input('Enter class start time in 24 hour format: (HH:MM) ')

    # Get the class finishing time
    class_finish = input('Enter class finish time in 24 hour format: (HH:MM) ')

    # Check time input
    while not (validate_time_input(class_finish)):
        print("\nInvalid input. Please try again")
        class_finish = input('Enter class finish time in 24 hour format: (HH:MM) ')

    # Add data to the database
    add_data_to_schedule_DB(class_codes, week_day, class_start, class_finish)


# Validate day of the week input
def validate_week_days_input(day):
    # Days of the week
    week_days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

    # Check if days input are correct
    if day.lower() in week_days:
        return True
    else:
        return False


# Validate time input
def validate_time_input(time):
    # Check if the time input is in time form
    if not re.match("\d\d:\d\d", time):
        return False
    # Return true if the input is in time form
    return True


# Validate date input
def validate_date_input(date):
    # Check if the time input is in time form
    if not re.match("\d\d/\d\d/\d\d", date):
        return False
    # Return true if the input is in time form
    return True


# Create schedule
#get_and_add_schedule()

