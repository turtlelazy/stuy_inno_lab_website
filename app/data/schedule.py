from data.data_functions import calendar
from datetime import datetime
import calendar as calendarLib
import json
def get_calendar(year,month):
    return calendar.get_main_value_from_conditions(["year","month"],[year,month])[0]

def calendar_exists(year,month):
    return calendar.get_main_value_from_conditions(["year", "month"], [year, month]) != None

def create_calendar(year,month,schedule_JSON):
    calendar.add_values([schedule_JSON,year, month])

def edit_calendar(year,month,schedule_JSON):
    calendar.delete_value_from_conditions(["year", "month"], [year, month])
    create_calendar(year,month,schedule_JSON)

def admin_calendar_creation(year,month,default_Schedule_JSON):
    #schedule_JSON is a list of the schedules in the days of the week from Monday to Sunday, as a list of dictionaries
    #Monday is 0 and Sunday is 6
    calendar_JSON = []
    schedule = json.loads(default_Schedule_JSON)

    for day in range(daysInMonth(year,month)):
        real_day = day + 1
        weekday = getWeekday(year,month,real_day)
        calendar_JSON.append(schedule[weekday])
    
    calendar_JSON = json.dumps(calendar_JSON)

    create_calendar(year,month,calendar_JSON)

def compile_calendar():
    calendar_JSON = []

    for month in calendar.get_all_values():
        calendar_JSON.append({
            "schedule": json.loads(month[0]),
            "year":month[1],
            "month":month[2]
        })

    return calendar_JSON


#helper functions
def daysInMonth(year, month):
    monthObject = datetime(year, month, 1)
    return calendarLib.monthrange(monthObject.year, monthObject.month)[1]

def getWeekday(year,month,day):
    return datetime(year,month,day).weekday()