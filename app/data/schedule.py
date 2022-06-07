from data.data_functions import calendar

def get_calendar(year,month):
    return calendar.get_main_value_from_conditions(["year","month"],[year,month])[0]

def create_calendar(year,month,schedule_JSON):
    calendar.add_values([schedule_JSON,year, month])
