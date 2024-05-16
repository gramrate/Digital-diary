def check_name_into_database(name, surname, fatname, all_users):
    for user in all_users:
        if user.name == name and user.surname == name and user.fatname == fatname:
            return True
    else:
        return False