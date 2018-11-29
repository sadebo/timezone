#!/usr/bin/env python3.7

import pytz
import datetime
import ntplib
import time
import calendar
import sys


user_tz = input("Enter the TimeZone, the default is (US/Eastern) if you press the Enter key: ") or "US/Eastern"
try:
    LOCALTIMEZONE = pytz.timezone(user_tz) # time zone name from Olson database
except:
    print ("Please check the timezone entered. It appears to be invalid!!!")
    sys.exit(1)

#Function to get seconds
def get_sec(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

def utc_to_local(utc_dt):
    try:
        return utc_dt.replace(tzinfo=pytz.utc).astimezone(LOCALTIMEZONE)
    except:
        return "Please check the timezone entered. It appears to be invalid!!!"
        sys.exit(1)

#Function to get the time according to the TimeZone
def get_time_from_NTPClient():
    from time import ctime
    try:
        c = ntplib.NTPClient()
        response = c.request('pool.ntp.org', version=3)
        formatted_date_with_micro_seconds =    datetime.datetime.strptime(str(datetime.datetime.utcfromtimestamp(response.tx_time)),"%Y-%m-%d %H:%M:%S.%f")
        local_dt = utc_to_local(formatted_date_with_micro_seconds)
        return local_dt
        #return datetime.datetime.strftime(local_dt, "%A, %b %d, %Y")
        #print (datetime.datetime.strftime(local_dt, "%A, %b %d, %Y"))

    except:
        print ("Issue with Time Sync!")
        return "Issue wth Time Sync"


def convert24(str1): 
      
    # Checking if last two elements of time 
    # is AM and first two elements are 12 
    if str1[-2:] == "AM" and str1[:2] == "12": 
        return "00" + str1[2:-2] 
          
    # remove the AM     
    elif str1[-2:] == "AM": 
        return str1[:-2] 
      
    # Checking if last two elements of time 
    # is PM and first two elements are 12    
    elif str1[-2:] == "PM" and str1[:2] == "12": 
        return str1[:-2] 
          
    else: 
        # add 12 to hours and remove PM 
        return (str(int(str1[:2]) + 12) + str1[2:6]).replace(':','')

#Define all variables that will be included in the print statements
#Get the current time
try:
    formatted_date = get_time_from_NTPClient()
    #Format to get Hours, Mins and Seconds
    time_in_digital = datetime.datetime.strftime(formatted_date, "%H:%M:%S")
    #Format to get Hours and Seconds
    time_in_digital_hrs_mins = datetime.datetime.strftime(formatted_date, "%I:%M %p")
    time_in_military_hrs_mins = convert24(time_in_digital_hrs_mins)
    #Get the number of Seconds
    time_in_sec_total = get_sec(time_in_digital)
    time_comma = "{:,}".format(time_in_sec_total)
    #Calculate the # of seconds left 86400 is a constant
    remain_time_sec = round((1 - (time_in_sec_total/86400)) *  100,2)


    today = datetime.date.today()
    days_in_current_month = calendar.monthrange(today.year, today.month)[1]
    days_end_month = days_in_current_month - int(datetime.datetime.strftime(formatted_date, "%d"))
    current_time = datetime.datetime.strftime(formatted_date, "%A, %b %d, %Y")

    #print(convert24(time_in_digital_hrs_mins))

    #print (days_end_month)
    #print(current_time)
    #print(time_in_sec_total)
    #print(remain_time_sec)
    #print (current_time)
    #print (time_comma)
    print (f'{current_time}.There are {days_end_month} left in the month')
    print (f'{time_in_digital_hrs_mins} or {time_in_military_hrs_mins}hours')
    print (f'{time_comma} seconds since midnight')
    print (f'{remain_time_sec}% of the day remains')
    #print (datetime.datetime.strftime(formatted_date, "%A, %b %d, %Y"))
except:
    print ("Something is wrong with the Code. Please contact Sanu Adebo!!!")
