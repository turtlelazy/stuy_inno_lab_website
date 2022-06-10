from data.data_functions import users
import bcrypt as b


def get_usernames():
    return users.get_main_values()


def get_emails():
    return users.get_main_values()

def user_exists(email):
    return email in get_emails()

def create_user(email, username,password,user_type):
    if(user_exists(email)):
        return False
    
    salt = b.gensalt()
    hashed = b.hashpw(password.encode('utf-8'), salt)

    users.add_values([email, username,hashed,salt,user_type])
    return True

def admin_verification(email):
    return users.get_value(email,"user_type") == "admin"

def get_salt(email):
    return users.get_value(email,"salt")
def get_hash(email):
    return users.get_value(email,"hash")
# def get_email(username):
#     return users.get_value(username, "email")
def get_username(email):
    return users.get_value(email, "username")

def verify_user(email, password):
    if(not user_exists(email)):
        return False

    salt = get_salt(email)
    hashed = b.hashpw(password.encode('utf-8'), salt)

    return get_hash(email) == hashed


# print(user_exists("foo"))
