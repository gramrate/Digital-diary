from datetime import datetime, timedelta


def get_time():
    current_date = datetime.now()
    formatted_date = current_date.strftime("%d/%m/%Y")
    return formatted_date


def get_user_by_name(name, surname, fatname, all_users):
    for user in all_users:
        if user.name == name and user.surname == surname and user.fatname == fatname:
            return user


def add_one_day(date_string):
    date_object = datetime.strptime(date_string, "%d/%m/%Y")
    new_date_object = date_object + timedelta(days=1)
    return new_date_object.strftime("%d%m%Y")


def subtract_one_day(date_string):
    date_object = datetime.strptime(date_string, "%d/%m/%Y")
    new_date_object = date_object - timedelta(days=1)
    return new_date_object.strftime("%d%m%Y")


def get_weekday(date_str):
    date_obj = datetime.strptime(date_str, '%d/%m/%Y')
    return date_obj.weekday()
