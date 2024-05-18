def check_name_into_database(name, surname, fatname, all_users):
    for user in all_users:
        if user.name == name and user.surname == surname and user.fatname == fatname:
            return True
    else:
        return False

def get_user_by_name(name, surname, fatname, all_users):
    for user in all_users:
        if user.name == name and user.surname == surname and user.fatname == fatname:
            return user
