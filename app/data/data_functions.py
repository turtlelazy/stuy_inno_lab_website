from sqlite3 import connect
from data.table import Table
from random import *
data = connect("data.db", isolation_level=None, check_same_thread=False)

users = Table(data, "users", "username")

def get_userIDs():
    "retuns a list of usernames"
    return users.get_main_values()


def get_usernames():
    return users.get_field("username")
    #return users.get_value_list("username","?")


def user_exists(username):
    "returns true if user exists"
    return users.value_exists(username, "username")


def userID_exists(userID):
    return users.value_exists(userID, "userID")


def getUsernameByID(userID):
    return users.get_value(userID, "username")


def getIDbyUsername(username):
    return users.get_non_main_value("username", username, "userID")[0]


def correct_password(username, password):
    "returns true if username matches password"
    try:
        real_password = users.get_value(getIDbyUsername(username), "password")
        return password == real_password
    except:
        return False


def add_user(username, password):
    "adds a user with username and passsowrd"

    x = randint(0, 1000)
    while(userID_exists(str(x))):
        x = randint(0, 1000)

    # while x in user_ID_list:
    #     x = randint(0, 1000)

    # user_ID_list.append(x)
    users.add_values([x, username, password])

def reset_data():
    "resets the database to empty user and story tables"
    open("tmp/data.db", "w").close()
    users.create(["username", "hash","salt","user_type"])
