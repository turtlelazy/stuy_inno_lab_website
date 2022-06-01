from data_functions import users
import bcrypt as b


def get_usernames():
    return users.get_main_values()

def user_exists(username):
    return username in get_usernames()

def create_user(username,password,user_type):
    if(user_exists(username)):
        return False
    
    salt = b.gensalt()
    hashed = b.hashpw(password,salt)

    users.add_values([username,hashed,salt,user_type])
    return True

def get_salt(username):
    return users.get_value(username,"salt")
def get_hash(username):
    return users.get_value(username,"hash")

def verify_user(username,password):
    if(not user_exists(username)):
        return False

    salt = get_salt(username)
    hashed = b.hashpw(password,salt)
    
    return get_hash(username) == hashed