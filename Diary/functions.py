from datetime import datetime, timedelta


def get_time():
    current_date = datetime.now()
    formatted_date = current_date.strftime("%d/%m/%Y")
    return formatted_date


def get_user_by_name(name, Users):
    surname, name, fatname = name.split()
    user = Users.query.filter_by(surname=surname, name=name, fatname=fatname).first()
    if not user:
        return None
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

def get_name_by_id(user_id, Users):
    user = Users.query.filter_by(user_id=user_id).first()
    if not user:
        return None
    return f'{user.surname} {user.name} {user.fatname}'


def get_classes_for_teacher(user_id, Schedule):
    lessons = Schedule.query.filter_by(teacher_user_id=user_id)
    return list({(lesson.class_num, lesson.class_let) for lesson in lessons})


def get_ratings_by_teacher(student_id, teacher_id, Rating, Schedule):
    rating = Rating.query.filter_by(user_id=student_id)
    rates = []
    for rate in rating:
        lesson = Schedule.query.filter_by(id=rate.lesson_id).first()
        if lesson and teacher_id == lesson.teacher_user_id:
            rates.append(rate)

    return rates