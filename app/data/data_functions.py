import sched
from sqlite3 import connect
from data.table import Table
from random import *
data = connect("data.db", isolation_level=None, check_same_thread=False)

users = Table(data, "users", "email")
calendar = Table(data, "calendar", "schedule")
machines = Table(data, "machines", "machine_name")

def reset_data():
    "resets the database to empty user and story tables"
    open("data.db", "w").close()
    users.create(["email","username", "hash","salt","user_type"])
    calendar.create(["schedule","year", "month"])
    # machines.create(["machine_name", "username", "time", "in_use"])
