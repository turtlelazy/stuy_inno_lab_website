from data.data_functions import reservations
from random import *

def rID_exists(id):
    return reservations.value_exists(id,"userID")

def get_latest(machine):
    t = reservations.get_main_value_from_conditions(["machine_name", "in_use"],[machine,1])
    if t == None:
        return "not in use"
    else:
        return t[0]
    
def machine_column(machine):
    c = []
    id = get_latest(machine)
    if id == "not in use":
        c = ['','',"not in use"]
        return c
    username = get_username(id)[0]
    time = get_time(id)[0]
    in_use = "currently in use"
    c.append(username)
    c.append(time)
    c.append(in_use)
    return c 

def get_username(id):
    return reservations.get_non_main_value("id",id,"username")

def get_time(id):
    return reservations.get_non_main_value("id",id,"time")


def new_reservations(username, machine, time):
    in_use = 1
    reservations.add_values([None, machine, username, time, in_use])
    return True


def end_reservations(machine):
    id = get_latest(machine)
    reservations.update_value('in_use', 0, id)

def see_reservations():
    reservations.get_all_values()

def get_opp():
    return reservations.get_main_values()

def get_machines():
    return reservations.get_field("machine_name")

def get_use():
    return reservations.get_field("in_use")