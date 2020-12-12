# Import libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import datetime
from datetime import datetime
import schedule
import time
import sqlite3
import re
import create_schedule


# Chrome options
opt = Options()

# Pass the argument 1 to allow and 2 to block
opt.add_experimental_option("prefs", {
    "profile.default_content_setting_values.media_stream_mic": 1,
    "profile.default_content_setting_values.media_stream_camera": 1,
    "profile.default_content_setting_values.geolocation": 2,
    "profile.default_content_setting_values.notifications": 2
  })


# Webdriver
driver = None

# Sign in credential
CREDS = {'email': 'myemail@gmail.com', 'passwd': 'mypassword'}

# Name of the link to enter the virtual class
common_names = ['VIRTUAL ROOM', 'BB Coll Ultra']


# View schedule
def view_schedule():
    # Database connection
    conn = sqlite3.Connection('schedule.db')

    # Database cursor
    c = conn.cursor()

    # View all the schedule data
    for row in c.execute('SELECT * FROM schedule ORDER BY classCode'):
        print(row)

    # Close connection
    conn.close()


# Sign in to website
def sign_in():
    # Driver variable
    global driver

    # Wait until the sign in button is present
    try:
        # Wait until the sign in button is present
        signIn = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "submitButton"))
        )

        # Print feedback
        print('Logging In')

        # Sign in (username)
        time.sleep(3) # Wait 3 sec
        username = driver.find_element_by_id('userNameInput') # Username
        username.send_keys(CREDS['email']) # Send username info

        # Sign in (password)
        time.sleep(3) # Wait 3 sec
        password = driver.find_element_by_id('passwordInput') # Password
        password.send_keys(CREDS['passwd']) # Send password info

        # Click sign in button
        time.sleep(5) # Wait 5 sec
        signIn.click() # Click sign in button

        # Print feedback
        print('Your are in')

        # Privacy agreement
        accept_privacy_agreement()

    except:
        # Close website
        driver.quit()


# Accept privacy agreement if appear
def accept_privacy_agreement():
    # Driver variable
    global driver

    # Wait until the agreement privacy is present
    try:
        # Wait until the agreement privacy appear
        privacy_agreement = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "agree_button"))
        )

        # Accept privacy agreement
        time.sleep(2) # Wait 2 sec
        privacy_agreement.click() # Accept privacy agreement

        # Print feedback
        print('Privacy agreement was accepted')

    except:
        # Print feedback
        print('There was not a privacy agreement prompt')


# Go to courses
def find_courses(course, class_start, class_finish):
    # Driver variable
    global driver

    # Wait until the course tab is present
    try:
        # Wait until the course tap appear
        course_tab = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Courses"))
        )

        # Click the link
        time.sleep(3) # Wait 3 sec
        course_tab.click() # Click the link

        # Print feedback
        print('Courses tab was click')

        try:
            # Wait until the course list appear
            courses_list = WebDriverWait(driver, 8).until(
                EC.presence_of_element_located((By.CLASS_NAME, "portletList-img"))
            )

            # Courses name list
            course_available = []

            # Get the courses name
            for name in courses_list.text.split('\n'):
                # Add the courses name to a list
                course_available.append(name)

            # Print courses name
            print('Your courses are {}'.format(course_available))

            # Check if the courses enter by the user are in the BlackBoard courses
            for i in course_available:
                if course.lower() == i.lower():
                    print("JOINING CLASS ", course)

                    # Navigate through courses
                    navigate_through_course(course, class_start, class_finish)
                    break

            # Print feedback
            #print('You are in course {}'.format(course_name[1]))

        except:
            # Print feedback
            print('I can not find the courses link')

    except:
        # Print feedback
        print('I could not find the courses tab link')


# Navigate through courses
def navigate_through_course(course, class_start, class_finish):
    # Driver variable
    global driver

    # Find course link to enter to the class
    enter_course = driver.find_element_by_link_text(course)

    # Click the link
    time.sleep(3) # Wait 3 sec
    enter_course.click() # Click the link

    try:
        # Wait until the virtual room appear
        class_content = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'courseMenuPalette_contents'))
        )

        # Variables
        class_content_list = []  # List for the content names of the class
        class_link_name = ' '  # Link name to join the virtual class
        flag = 0  # Flag just to check if the class contain a link or nor for vc (0=not, 1=yes)

        # Get all the content name of the class
        for content in class_content.text.split('\n'):
            # Add the content to the list
            class_content_list.append(content)

        print(class_content_list)

        # Check each value in common names list
        for commonNames in common_names:
            # Get length range for the class content list
            for x in range(len(class_content_list)):
                # Check if a name in common name list is in the class content list
                if commonNames == class_content_list[x]:
                    # Assign value to the variable
                    class_link_name = class_content_list[x]
                    flag = 1
                    break

        # Check if there is a link for the virtual class or no
        if flag == 0:
            # Print feedback
            print('Sorry, your professor did not put the class link here.')
            print('You should enter the class through the link that your professor sent you.')
            print('I will sign you out and close the website for you.')

            # Sign out - close website and browser
            sign_out()

        else:
            print('The link for the class is in (%s)' % class_link_name)

            try:

                # Wait until the virtual room appear
                virtual_room = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.LINK_TEXT, class_link_name))
                )

                # Click the link
                time.sleep(4)  # Wait 4 sec
                virtual_room.click()  # Click the link

                # Join class
                join_class(class_start, class_finish)

                # Switch back to default frame
                # driver.switch_to.default_content()

                # Print feedback
                print('Your are in default iframe')

            except:
                # Print feedback
                print('I can not find the virtual room link')

    except:
        print('I could not find the class content')


# Join class link
def join_class(class_start, class_finish):
    # Driver variable
    global driver

    # Switch to BlackBoard Collab iframe
    driver.switch_to.frame('collabUltraLtiFrame')
    print('Your are in BlackBoard Collab iframe')

    try:
        # Wait until the class link button appear
        class_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "item-list__item"))
        )

        # Click the button
        time.sleep(4) # Wait 4 sec
        class_link.click() # Click the button

        try:
            # Wait until the class link button appear
            join_class_link = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="offcanvas-wrap"]/div[2]/div/div/div/div/div[2]/div/bb-loading-button/button'))
            )

            # Click the button
            time.sleep(4) # Wait 4 sec
            join_class_link.click() # Click the button

            # Print feedback
            print('You join the class')

            # Virtual classroom
            virtual_class_room(class_start, class_finish)

            time.sleep(5)

            # Virtual class window
            blackboard_window = driver.window_handles[0]
            driver.switch_to.window(blackboard_window) # Switch to virtual class window
            print('We are in class window')

            #driver.switch_to.default_content()

        except:
            # Print feedback
            print('Can not access the class link')

    except:
        # Print feedback
        print('Can not enter to the virtual room')


# Switch to virtual room tap and attend class live video
def virtual_class_room(start_time, finish_time):
    # Driver variable
    global driver

    # Virtual class window
    class_room_window = driver.window_handles[1]

    # Switch to virtual class window
    driver.switch_to.window(class_room_window)
    print('We are in class window')

    # Accept every prompt when you start the class for first time
    accept_prompt_when_enter_vr()

    # Schedule leaving class time
    tmp = "%H:%M"
    class_running_time = datetime.strptime(finish_time, tmp) - datetime.strptime(start_time, tmp) # Find out how many hours do we have left for the class
    print("Your class will finish in {} seconds, that is {}".format(class_running_time.seconds, class_running_time)) # Print result in seconds
    time.sleep(class_running_time.seconds) # Sleep until the class finish

    # Exit virtual class window
    exit_virtual_class_room()

    # Close class room window
    time.sleep(5)
    driver.close() # Close just the tab
    print('I close the class room window')


# Accept everything when you enter the virtual class room
def accept_prompt_when_enter_vr():
    # Driver variable
    global driver

    # Audio check
    try:
        # Wait until the audio check appear
        accept_audio_check = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="dialog-description-audio"]/div[2]/button'))
        )

        # Click the button
        time.sleep(4)
        accept_audio_check.click()

        # Video check
        try:
            # Wait until the video check appear
            accept_video_check = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="techcheck-video-ok-button"]'))
            )

            # Click the button
            time.sleep(4)
            accept_video_check.click()

            # Tutorial
            try:
                # Wait until the video check appear
                later_tutorial = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="announcement-modal-page-wrap"]/div/div[4]/button'))
                )

                # Click the button
                time.sleep(4)
                later_tutorial.click()

                # Close something
                try:
                    # Wait until the video check appear
                    close_something = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located(
                            (By.XPATH, '//*[@id="tutorial-dialog-tutorials-menu-learn-about-tutorials-menu-close"]'))
                    )

                    # Click the button
                    time.sleep(4)
                    close_something.click()

                except:
                    # Print feedback
                    print('There was not a Close something.')

            except:
                # Print feedback
                print('There was not a tutorial.')

        except:
            # Print feedback
            print('There was not a video check.')

    except:
        # Print feedback
        print('There was not a audio check.')


# Exit virtual class room
def exit_virtual_class_room():
    # Driver variable
    global driver

    # Exit virtual class
    try:
        # Wait until the menu button appear
        open_menu = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'session-menu-open'))
        )

        # Click the button
        time.sleep(4)
        open_menu.click()

        # Leave session
        try:
            # Wait until the leave session appear
            leave_session = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'leave-session'))
            )

            # Click the button
            time.sleep(4)
            leave_session.click()

            # Skip session survey
            try:
                # Wait until the survey session appear
                skip_survey_session = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, 'session-survey-skip'))
                )

                # Click the button
                time.sleep(4)
                skip_survey_session.click()

            except:
                # Print feedback
                print('I could not skip survey session.')

        except:
            # Print feedback
            print('I could not leave the session.')

    except:
        # Print feedback
        print('I could not find the menu option.')


# Logout from website
def sign_out():
    # Driver variable
    global driver

    try:
        # Wait until the logout button appear
        logout = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.ID, 'topframe.logout.label'))
        )

        # Click the button
        time.sleep(4)  # Wait 4 sec
        logout.click()  # Click the button

        try:
            # Wait until the end session button appear
            end_session = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.ID, 'end'))
            )

            # Click the button
            time.sleep(3) # Wait 3 sec
            end_session.click() # Click the button

            try:
                # Wait until the close session button appear
                close_session = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/p/input[2]'))
                )

                # Click the button
                time.sleep(2) # Wait 2 sec
                close_session.click() # Click the button
                print('Session Close') # Print feedback

                # Close website and browser
                close_website()

            except:
                print('Didnt see the final botton')

        except:
            # Print feedback
            print('I could not end session')

    except:
        # Print feedback
        print('I could not logout from the website')


# Close website
def close_website():
    # Driver variable
    global driver

    # Delete all the cookies before closing website
    #driver.delete_all_cookies()

    time.sleep(5) # Wait 5 sec
    driver.quit() # Close browser

    # Print feedback
    print('Website close')


# Website and driver setup
def start_browser():
    # Driver variable
    global driver

    # Driver
    PATH = 'driver/chromedriver' # Driver path
    driver = webdriver.Chrome(options=opt, executable_path=PATH) # Chrome driver

    # Open website
    URL = 'https://mdc.blackboard.com/' # Website url
    driver.get(URL) # Open website

    driver.maximize_window() # Maximize window

    # Sign in in the website
    sign_in()

    # Return driver
    #return driver_


# Class schedule
def class_schedule():
    # Database connection
    conn = sqlite3.connect('schedule.db') # DB connection
    c = conn.cursor() # DB cursor

    # Get every data in DB
    for row in c.execute('SELECT * FROM schedule'):
        # Schedule data
        name = row[0] # Class code
        day = row[1] # Day of the week
        start_time = row[2] # Class start time
        end_time = row[3] # Class end time

        # Check if there are more than one day
        if re.search(', ', day):
            # Different days of the class
            days = day.split(', ')

            # Make schedule for every day of the class
            for day_ in days:
                # Make schedule
                make_schedule(name, day_, start_time, end_time)
        else:
            # Make schedule
            make_schedule(name, day, start_time, end_time)

    # Start browser
    start_browser()

    while True:
        # Checks whether a scheduled task
        # is pending to run or not
        schedule.run_pending()
        time.sleep(1)


# Make schedule
def make_schedule(name, day, start_time, end_time):
    # Class schedule
    if day.lower() == "monday":
        schedule.every().monday.at(start_time).do(find_courses, name, start_time, end_time)
        print("Scheduled class '%s' on %s at %s" % (name, day, start_time))
    if day.lower() == "tuesday":
        schedule.every().tuesday.at(start_time).do(find_courses, name, start_time, end_time)
        print("Scheduled class '%s' on %s at %s" % (name, day, start_time))
    if day.lower() == "wednesday":
        schedule.every().wednesday.at(start_time).do(find_courses, name, start_time, end_time)
        print("Scheduled class '%s' on %s at %s" % (name, day, start_time))
    if day.lower() == "thursday":
        schedule.every().thursday.at(start_time).do(find_courses, name, start_time, end_time)
        print("Scheduled class '%s' on %s at %s" % (name, day, start_time))
    if day.lower() == "friday":
        schedule.every().friday.at(start_time).do(find_courses, name, start_time, end_time)
        print("Scheduled class '%s' on %s at %s" % (name, day, start_time))
    if day.lower() == "saturday":
        schedule.every().saturday.at(start_time).do(find_courses, name, start_time, end_time)
        print("Scheduled class '%s' on %s at %s" % (name, day, start_time))
    if day.lower() == "sunday":
        schedule.every().sunday.at(start_time).do(find_courses, name, start_time, end_time)
        print("Scheduled class '%s' on %s at %s" % (name, day, start_time))


# Main function
def main():

    # Create and add schedule to database
    create_schedule.get_and_add_schedule()

    # View schedule
    view_schedule()

    # Find course and join class (You can use this to text the code without the schedule
    #find_courses('PHY2049-2207-6214', '10:00', '10:01')

    # Class schedule
    class_schedule()

    time.sleep(5)

    # Sign out
    sign_out()


# Run the bot
main()


