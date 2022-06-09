from data.machines import *
from data.users import *
from data.data_functions import *
# reset_data()

# new_reservations("r", "laser", 9)
# new_reservations("s", "cnc", 7)
# new_reservations("b", "3pd 1", 2)
# new_reservations("g", "3pd 2", 7)


# create_user("email2","userna2me","passwor2d","adm2in")

# id = get_latest("3pd 1")
# end_reservations("laser")

# print("id")
# print(id)


# print("all ids")
# print(get_username("naominaranjonn@gmail.com"))

rows = get_machines()

# print("machine_names")
for r in rows:
    print(r)

# print("uses")
# rows = get_use()

# for r in rows:
#     print(r)

# print(get_latest("laser"))

# print("cnc column")
# print(machine_column("cnc"))
# print("3dp 1 column")
# print(machine_column("3pd 1"))
# print("laser column")
# print(machine_column("laser"))