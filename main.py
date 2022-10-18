from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import os
import datetime

# os.popen('chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\\Users\\BETA\\Desktop"')

csv_file = 'AutoFastQC_-_EM_-_em_regular_source.csv'

option = webdriver.ChromeOptions()
option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(options=option)

data = pd.read_csv(csv_file, skiprows=3)

with open(csv_file, 'r') as f:
    dat = f.read()
    Cohort_name = dat.split(',')[1]
    Start_date = dat.split('\n')[1].split(',')[1]
    End_date = dat.split('\n')[2].split(',')[1]
    print('Cohort Name =', Cohort_name)
    print('Start date =', Start_date)
    print('End date =', End_date)

weblinkcohorts = 'https://uplevel.interviewkickstart.com/cohorts/'
weblinksGC = 'https://uplevel.interviewkickstart.com/app/a/global-calendar'


def find_and_click(xpath):
    time.sleep(0.5)
    ITEM = driver.find_element(By.XPATH, xpath)
    time.sleep(0.5)
    ITEM.click()


def fill_form(xpath, text):
    OBJ = driver.find_element(By.XPATH, xpath)
    OBJ.click()
    OBJ.clear()
    OBJ.send_keys(text)
    time.sleep(1)
    OBJ.send_keys(Keys.RETURN)
    time.sleep(1)


def down_enter(xpath):
    time.sleep(0.5)
    ELEMENT = driver.find_element(By.XPATH, xpath)
    ELEMENT.send_keys(Keys.DOWN)
    ELEMENT.send_keys(Keys.RETURN)
    time.sleep(0.5)


def search_for_cohort():
    driver.get(weblinkcohorts)

    fill_form('/html/body/div[1]/div[2]/div/div[2]/div/div[1]/div[3]/div/label/input', Cohort_name)
    time.sleep(2)

    print("Reading output")

    TABLE = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div/div[2]/table/tbody')
    print(len(TABLE.find_elements(By.TAG_NAME, 'h6')), 'data rows found')

    TABLE_TEXTS = list((item.text for item in TABLE.find_elements(By.TAG_NAME, 'h6')))

    if Cohort_name + ' [do not use]' in TABLE_TEXTS:  # check if found upon searching
        print('Search results')
        for item in TABLE.find_elements(By.TAG_NAME, 'h6'):
            print(item.text)
            if item.text == str(Cohort_name + ' [do not use]'):
                print("Clicking on", item.text)
                item.click()
                break
        time.sleep(1)
        discarding_cohort()


def discarding_cohort():
    COHORT_NAME = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/form/div[2]/div/div/div[1]/input')
    COHORT_NAME.click()
    COHORT_NAME.clear()
    COHORT_NAME.send_keys(Cohort_name + ' [do not use]')
    COHORT_NAME.send_keys(Keys.RETURN)

    ISENROLLMENTCLOSED = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/form/div[2]/div/div/div[4]/div[2]/div/div/label')
    if ISENROLLMENTCLOSED.text == "No":
        ISENROLLMENTCLOSED.click()
        time.sleep(1)

    TESTLEADS = driver.find_element(By.XPATH,
                                    '/html/body/div[1]/div[2]/div/div[2]/form/div[2]/div/div/div[10]/div/label')
    if TESTLEADS.text == "No":
        TESTLEADS.click()
        time.sleep(1)

    SAVE = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/form/div[3]/div/div/div/button')
    SAVE.click()
    time.sleep(1)


def create_new_cohort():
    driver.get(weblinkcohorts)
    time.sleep(3)

    # CREATE_NEW = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/div[2]/a[1]')
    # CREATE_NEW.click()

    fill_form('/html/body/div[1]/div[2]/div/div[2]/form/div[2]/div/div/div[1]/input', Cohort_name)

    COHORT_COUNTRY = driver.find_element(By.XPATH,
                                         '/html/body/div[1]/div[2]/div/div[2]/form/div[2]/div/div/div[2]/span/span[1]/span/span[1]')  # dropdown
    COHORT_COUNTRY.click()
    time.sleep(1)
    USA = driver.find_element(By.XPATH, '/html/body/span/span/span[2]/ul/li[2]')
    USA.click()
    time.sleep(1)

    fill_form('/html/body/div[1]/div[2]/div/div[2]/form/div[2]/div/div/div[3]/div[1]/div/input', Start_date)
    fill_form('/html/body/div[1]/div[2]/div/div[2]/form/div[2]/div/div/div[3]/div[2]/div/input', End_date)
    fill_form('/html/body/div[1]/div[2]/div/div[2]/form/div[2]/div/div/div[4]/div[1]/div/input', '50')

    ASSOCIATEDWITHPROGRAM = driver.find_element(By.XPATH,
                                                '/html/body/div[1]/div[2]/div/div[2]/form/div[2]/div/div/div[5]/span/span[1]/span/span[1]/span')
    ASSOCIATEDWITHPROGRAM.click()
    time.sleep(1)
    fill_form('/html/body/span/span/span[1]/input', 'Engineering Management Program')

    fill_form('/html/body/div[1]/div[2]/div/div[2]/form/div[2]/div/div/div[8]/input', 'www.zoom.us')

    # SAVE = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/form/div[3]/div/div/div/button')
    # SAVE.click()


def scheduling():
    # driver.get(weblinksGC)
    # time.sleep(3)

    temp = {'resourcecollection': 'Resource Collection',
            'feedbacktemplate': 'Feedback',
            'class': 'Class',
            'test': 'Test',
            'video': 'Video',
            'instruction': 'Instruction',

            'On Scheduled Date': 'Active on Schedule',
            'Always active': 'Always Active',
            'Conditional': 'Conditional'
            }

    for i in range(len(data)):
        SCHEDULE = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[3]/div[2]/div/div/button/span[2]')
        SCHEDULE.click()

        TABLE = driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/ul/div/div')
        for item in TABLE.find_elements(By.TAG_NAME, 'div'):
            if item.text == temp[data['Type Name'][i]]:
                print(f'Clicking {item.text}')
                item.click()
                break

        TOPIC = '/html/body/div[2]/div[3]/div/div[1]/div[1]/div/div[1]/div[2]/div[1]/div/div/div/input'
        find_and_click(TOPIC)
        fill_form(TOPIC, data['Topic Name'][i])
        down_enter(TOPIC)

        RESOURCE = '/html/body/div[2]/div[3]/div/div[1]/div[1]/div/div[1]/div[2]/div[2]/div/div/div/input'
        find_and_click(RESOURCE)
        fill_form(RESOURCE, data['Resource Name'][i])
        down_enter(RESOURCE)

        START_DATE = '/html/body/div[2]/div[3]/div/div[1]/div[1]/div/div[2]/div[2]/div[1]/div/div/input'
        find_and_click(START_DATE)
        Start_date = datetime.datetime.strptime(data['Start Date'][i], '%Y-%m-%d').strftime('%m/%d/%Y')
        fill_form(START_DATE, Start_date)

        START_TIME = '/html/body/div[2]/div[3]/div/div[1]/div[1]/div/div[2]/div[2]/div[2]/div/div/div/input'
        find_and_click(START_TIME)
        Start_time = datetime.datetime.strptime(data['Start Time'][i], '%H:%M:%S').strftime('%H:%M:%S')
        fill_form(START_TIME, Start_time)

        if len(str(data['End Time'][i])) != 3:
            print('Has End time')
            ENDTIMETOGGLE = '/html/body/div[2]/div[3]/div/div[1]/div[1]/div/div[2]/div[1]/div/label/span[2]/span/div'
            find_and_click(ENDTIMETOGGLE)

            END_DATE = '/html/body/div[2]/div[3]/div/div[1]/div[1]/div/div[2]/div[2]/div[3]/div/div/input'
            find_and_click(END_DATE)
            End_date = datetime.datetime.strptime(data['End Date'][i], '%Y-%m-%d').strftime('%m/%d/%Y')
            fill_form(END_DATE, End_date)

            END_TIME = '/html/body/div[2]/div[3]/div/div[1]/div[1]/div/div[2]/div[2]/div[4]/div/div/div/input'
            find_and_click(END_TIME)
            End_time = datetime.datetime.strptime(data['End Time'][i], '%H:%M:%S').strftime('%H:%M:%S')
            fill_form(END_TIME, End_time)
        else:
            print('does not have end time')

        FOR = '/html/body/div[2]/div[3]/div/div[1]/div[1]/div/div[3]/div[2]/div/div/input'
        fill_form(FOR, Cohort_name)
        down_enter(FOR)

        ACTIVE = '/html/body/div[2]/div[3]/div/div[1]/div[1]/div/div[4]/div[2]/div[2]'
        for item in driver.find_element(By.XPATH, ACTIVE).find_elements(By.TAG_NAME, 'label'):
            if item.text == temp[data['Activity Status'][i]]:  # and data['Activity Status'][i] != 'Conditional'
                item.click()
                break

        # INSTRUCTIONS = '/html/body/div[2]/div[3]/div/div[1]/div[1]/div/div[5]/div[2]/div/div/div/div/div/input'
        # fill_form(INSTRUCTIONS, data['Activity'][i])
        # down_enter(INSTRUCTIONS)
        #
        # ADDTIONAL_DATA = '/html/body/div[2]/div[3]/div/h2/div/div/div[1]/div/div/div/button[2]'
        # find_and_click(ADDTIONAL_DATA)

        break


scheduling()

quit()
