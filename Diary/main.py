from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import exists
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required
from UserLogin import UserLogin
from flask import Flask, request, render_template, Response
from werkzeug.utils import secure_filename
from db import db_init, db
from models import *
from variables import MESSAGE_LIST, WEEKDAYS
from functions import *
import config

app = Flask(__name__)
app.config['SECRET_KEY'] = config.APP_SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQL_PATH

db_init(app)

login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id, Users)


@app.route('/666')  # расписание
@login_required
def sixsixsix():
    lesson = Schedule(class_num='10', class_let='A', subject_id=1, lesson_number=1, teacher_user_id=1, homework='no',
                      date='06/06/2024')
    db.session.add(lesson)
    lesson = Schedule(class_num='10', class_let='A', subject_id=1, lesson_number=2, teacher_user_id=1, homework='no',
                      date='06/06/2024')
    db.session.add(lesson)
    lesson = Schedule(class_num='10', class_let='A', subject_id=1, lesson_number=3, teacher_user_id=1, homework='no',
                      date='06/06/2024')
    db.session.add(lesson)
    lesson = Schedule(class_num='10', class_let='A', subject_id=1, lesson_number=4, teacher_user_id=1, homework='no',
                      date='06/06/2024')
    db.session.add(lesson)

    sub = Subjects(subject_name="Math")
    db.session.add(sub)
    sub = Subjects(subject_name="Russ")
    db.session.add(sub)
    sub = Subjects(subject_name="Gym")
    db.session.add(sub)
    sub = Subjects(subject_name="Eng")
    db.session.add(sub)
    sub = Subjects(subject_name="Chemst")
    db.session.add(sub)
    sub = Subjects(subject_name="IT")
    db.session.add(sub)

    student = Student(user_id=1, class_num='10', class_let='A')
    db.session.add(student)
    teacher = Teacher(user_id=2, subject_id=1)
    db.session.add(teacher)

    rating = Rating(user_id=1, subject_id=1, lesson_id=1, rate=5, date='06/06/2024', comment='no comment')
    db.session.add(rating)
    rating = Rating(user_id=1, subject_id=1, lesson_id=1, rate=2, date='06/06/2024', comment='no comment')
    db.session.add(rating)
    rating = Rating(user_id=1, subject_id=1, lesson_id=1, rate=4, date='06/06/2024', comment='no comment')
    db.session.add(rating)
    rating = Rating(user_id=1, subject_id=1, lesson_id=1, rate=3, date='06/06/2024', comment='no comment')
    db.session.add(rating)
    rating = Rating(user_id=1, subject_id=1, lesson_id=1, rate=5, date='06/06/2024', comment='no comment')
    db.session.add(rating)
    db.session.commit()
    return 'True'


@app.route('/777')
def sevsevsev():
    lesson = Schedule(class_num='10', class_let='A', subject_id=1, lesson_number=1, teacher_user_id=2, homework='no',
                      date='06/06/2024')
    db.session.add(lesson)
    db.session.commit()

    return 'True'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/schedule/<int:user_id>')  # расписание
@login_required
def schedule_redirect(user_id):
    return redirect(f'/schedule/0/{user_id}')


@app.route('/schedule/<date>/<int:user_id>')  # расписание
@login_required
def schedule(date, user_id):
    user = Users.query.filter_by(user_id=user_id).first()
    if not user:
        return render_template('notification.html', message=MESSAGE_LIST[5633], message_id=5633, url=f'/',
                               text='To main')
    if len(date) != 8:
        date = get_time()
        err_date = True
    else:
        date = date[:2] + '/' + date[2:4] + '/' + date[4:]
        err_date = False

    next_day = add_one_day(date)
    next_day = add_one_day(date)
    prev_day = subtract_one_day(date)
    weekday = WEEKDAYS.get(get_weekday(date))
    is_teacher = False
    if user.is_teacher:
        teacher = Teacher.query.filter_by(user_id=user_id).first()
        if not teacher:
            return render_template('notification.html', message=MESSAGE_LIST[5775], message_id=5775, url=f'/',
                                   text='To main')
        day = Schedule.query.filter_by(date=date, teacher_user_id=teacher.user_id)
        is_teacher = True

        # делать обработку на урок этого человека
    elif user.is_student:
        student = Student.query.filter_by(user_id=user_id).first()
        if not student:
            return render_template('notification.html', message=MESSAGE_LIST[5775], message_id=5775, url=f'/',
                                   text='To main')

        day = Schedule.query.filter_by(date=date, class_num=student.class_num, class_let=student.class_let)

    else:
        return render_template('notification.html', message=MESSAGE_LIST[8207], message_id=8207, url=f'/',
                               text='To main')

    if day.count():
        subjects = Subjects.query.all()
        all_subjects = ['null']
        for subj in subjects:
            all_subjects.append(subj.subject_name)
        return render_template('schedule.html', user_id=user_id, day=day, all_subjects=all_subjects, date=date,
                               err_date=err_date, next_day=next_day, prev_day=prev_day, weekday=weekday,
                               is_teacher=is_teacher)
    else:
        return render_template('schedule.html', user_id=user_id, empty_day=True, date=date, next_day=next_day,
                               prev_day=prev_day, weekday=weekday, is_teacher=is_teacher)


@app.route('/schedule/homework/<int:lesson_id>/<int:user_id>', methods=['POST', 'GET'])
@login_required
def schedule_homework(lesson_id, user_id):
    user = Users.query.filter_by(user_id=user_id).first()
    if not user:
        return render_template('notification.html', message=MESSAGE_LIST[8207], message_id=8207,
                               url=f'/schedule/0/{user_id}', text='Back to schedule')
    if user.is_teacher:
        lesson = Schedule.query.filter_by(id=lesson_id).first()
        if not lesson:
            return render_template('notification.html', message=MESSAGE_LIST[8609], message_id=8609,
                                   url=f'/schedule/0/{user_id}', text='To schedule')
        subject_obj = Subjects.query.filter_by(subject_id=lesson.subject_id).first()
        if not subject_obj:
            return render_template('notification.html', message=MESSAGE_LIST[8609], message_id=8609,
                                   url=f'/schedule/0/{user_id}', text='To schedule')
        subject = subject_obj.subject_name
        date = lesson.date
        class_num = lesson.class_num
        class_let = f'"{lesson.class_let}"'
        date_url = date.replace('/', '')
        if request.method == 'POST':
            homework = request.form['homework']

            if not homework:
                return render_template('schedule_homework.html', date=date, subject=subject, class_num=class_num,
                                       class_let=class_let, clear_fields=True)
            try:
                lesson.homework = homework
                db.session.commit()
                return render_template('notification.html', message=MESSAGE_LIST[8457], message_id=8457,
                                       url=f'/schedule/{date_url}/{user_id}', text='Back to schedule')
            except Exception as e:
                return render_template('notification.html', message=MESSAGE_LIST[4898], message_id=4898,
                                       url=f'/schedule/{date_url}/{user_id}', text='Back to schedule')
        else:
            return render_template('schedule_homework.html', date=date, subject=subject, class_num=class_num,
                                   class_let=class_let, homework=lesson.homework)
    else:
        return render_template('notification.html', message=MESSAGE_LIST[2776], message_id=2776,
                               url=f'/schedule/0/{user_id}', text='Back to schedule')


@app.route('/schedule/ratings/<int:lesson_id>/<int:user_id>', methods=['POST', 'GET'])  # расписание
@login_required
def schedule_rating(lesson_id, user_id):
    user = Users.query.filter_by(user_id=user_id).first()
    if not user:
        return render_template('notification.html', message=MESSAGE_LIST[5633], message_id=5633, url=f'/',
                               text='To main')
    if user.is_student:
        return render_template('notification.html', message=MESSAGE_LIST[2776], message_id=2776,
                               url=f'/ratings/{user_id}',
                               text='To ratings')
    elif user.is_teacher:
        lesson = Schedule.query.filter_by(id=lesson_id).first()
        if not lesson:
            return render_template('notification.html', message=MESSAGE_LIST[8609], message_id=8609,
                                   url=f'/schedule/0/{user_id}',
                                   text='To schedule')

        if request.method == 'POST':
            rate = request.form['rate']
            student = request.form['student']
            comment = request.form['comment']

            student = get_user_by_name(name=student, Users=Users)
            if not student:
                return render_template('notification.html', message=MESSAGE_LIST[4898], message_id=4898,
                                       url=f'/', text='To main')
            try:
                rate = Rating(user_id=student.user_id, subject_id=lesson.subject_id, lesson_id=lesson.id, rate=rate, date=lesson.date, comment=comment)
                db.session.add(rate)
                db.session.commit()
                return render_template('notification.html', message=MESSAGE_LIST[3870], message_id=3870,
                                       url=f'/schedule/{(lesson.date).replace("/", "")}/{user_id}',text='To schedule')
            except Exception as e:
                print(e)
                return render_template('notification.html', message=MESSAGE_LIST[4898], message_id=4898,
                                       url=f'/',text='To main')
        else:

            date = lesson.date.replace('/', '')
            all_students = Student.query.filter_by(class_num=lesson.class_num, class_let=lesson.class_let)
            students = []
            for stud in all_students:
                name = get_name_by_id(user_id=stud.user_id, Users=Users)
                if name: students.append(name)
            return render_template('schedule_rating.html', user_id=user_id, date=date, students=students)
    else:
        return render_template('notification.html', message=MESSAGE_LIST[4898], message_id=4898,
                               url=f'/',text='To main')


@login_required
@app.route('/ratings/<int:user_id>')  # оценки
def ratings(user_id):
    user = Users.query.filter_by(user_id=user_id).first()
    if not user:
        return render_template('notification.html', message=MESSAGE_LIST[5633], message_id=5633, url=f'/',
                               text='To main')
    # rating = Rating.query.filter_by(user_id=user_id)
    # if not len(rating):
    #     return render_template('notification.html', message=MESSAGE_LIST[5775], message_id=5775, url=f'/',
    #                            text='To main')

    all_subjects = Subjects.query.all()
    # all_subjects = []
    # all_ratings = ['null']
    # for subj in subjects:
    #     all_subjects.append(subj.subject_name)

    return render_template('ratings.html', user_id=user_id, all_subjects=all_subjects)


@login_required
@app.route('/ratings/<int:subject_id>/<int:user_id>')  # оценки
def ratings_of_subject(subject_id, user_id):
    user = Users.query.filter_by(user_id=user_id).first()
    if not user:
        return render_template('notification.html', message=MESSAGE_LIST[5633], message_id=5633, url=f'/',
                               text='To main')
    if user.is_teacher:
        return render_template('notification.html', message=MESSAGE_LIST[2776], message_id=2776,
                               url=f'/ratings/{user_id}',
                               text='To ratings')
    elif user.is_student:
        subject = Subjects.query.filter_by(subject_id=subject_id).first()
        if subject:
            subject_name = subject.subject_name
        else:
            subject_name = "Error"
        rating = Rating.query.filter_by(subject_id=subject_id, user_id=user_id)
        if len(list(rating)) == 0:
            return render_template('each_rating.html', user_id=user_id, no_rating=True, subject_name=subject_name)

        sredn = round(sum([subj.rate for subj in rating]) / len(list(rating)), 2)
        return render_template('each_rating.html', user_id=user_id, rating=rating, subject_name=subject_name,
                               sredn=sredn)


@login_required
@app.route('/ratings/each/<int:rate_id>/<int:user_id>')  # оценки
def each_rating_of_subject(rate_id, user_id):
    user = Users.query.filter_by(user_id=user_id).first()
    if not user:
        return render_template('notification.html', message=MESSAGE_LIST[5633], message_id=5633, url=f'/',
                               text='To main')
    if user.is_teacher:
        return render_template('notification.html', message=MESSAGE_LIST[2776], message_id=2776,
                               url=f'/ratings/{user_id}',
                               text='To ratings')
    elif user.is_student:
        rate = Rating.query.filter_by(id=rate_id).first()
        if not rate:
            return render_template('notification.html', message=MESSAGE_LIST[4454], message_id=4454,
                                   url=f'/ratings/{user_id}',
                                   text='To ratings')
        subject = Subjects.query.filter_by(subject_id=rate.subject_id).first()
        if subject:
            subject_name = subject.subject_name
        else:
            subject_name = "Error"

        return render_template('about_rate.html', user_id=user_id, susubject_name=subject_name, rate=rate.rate,
                               date=rate.date, comment=rate.comment, subject_id=rate.subject_id)


@app.route('/profile/<int:user_id>')  # Профиль
@login_required
def profile(user_id):
    user = Users.query.filter_by(user_id=user_id).first()
    if not user:
        return render_template('notification.html', message=MESSAGE_LIST[5633], message_id=5633, url=f'/',
                               text='To main')
    if user.is_student:
        student = Student.query.filter_by(user_id=user_id).first()
        if not student:
            class_num = 'You haven\'t been assigned to a class yet'
            class_let = ''
        else:
            class_num = student.class_num
            class_let = f'"{student.class_let}"'
        return render_template('profile.html', user_id=user_id, name=user.name, surname=user.surname,
                               fatname=user.fatname, is_student=True,
                               class_num=class_num, class_let=class_let)
    elif user.is_teacher:
        teacher = Teacher.query.filter_by(user_id=user_id).first()
        if teacher:
            subjects = Subjects.query.filter_by(subject_id=teacher.subject_id).first()
            if subjects:
                subject = subjects.subject_name
        else:
            subject = 'You haven\'t been assigned to subjects yet'

        return render_template('profile.html', user_id=user_id, name=user.name, surname=user.surname,
                               fatname=user.fatname, is_teacher=True,
                               subject=subject)
    else:
        return render_template('notification.html', message=MESSAGE_LIST[5775], message_id=5775, url=f'/',
                               text='To main')


@app.route('/profile/edit/<int:user_id>', methods=['POST', 'GET'])  # Профиль
@login_required
def profile_edit(user_id):
    user = Users.query.filter_by(user_id=user_id).first()

    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        fatname = request.form['fatname']

        type_user = request.form.get('type_user')
        is_teacher = True if type_user == 'teacher' else False
        is_student = not is_teacher

        if not all((name, surname, fatname, type_user)):
            return render_template('profile_edit.html', user_id=user_id, name=user.name, surname=user.surname,
                                   fatname=user.fatname, is_student=is_student, is_teacher=is_teacher,
                                   clear_fields=True)
        if Users.query.filter_by(name=name, fatname=fatname, surname=surname) and user.is_teacher != is_teacher:
            return render_template('profile_edit.html', user_id=user_id, name=user.name, surname=user.surname,
                                   fatname=user.fatname, is_student=is_student, is_teacher=is_teacher, user_exists=True)
        try:
            user.name = name
            user.surname = surname
            user.fatname = fatname
            user.is_student = is_student
            user.is_teacher = is_teacher
            db.session.commit()
            return render_template('notification.html', message=MESSAGE_LIST[3965], message_id=3965,
                                   url=f'/profile/{user_id}', text='Back to profile')
        except Exception as e:
            print(e)
            return render_template('notification.html', message=MESSAGE_LIST[4898], message_id=4898,
                                   url=f'/profile/{user_id}', text='Back to profile')

    else:
        if user:
            is_student = user.is_student
            is_teacher = user.is_teacher
            return render_template('profile_edit.html', user_id=user_id, name=user.name, surname=user.surname,
                                   fatname=user.fatname, is_student=is_student, is_teacher=is_teacher)
        else:
            return render_template('notification.html', message=MESSAGE_LIST[5633], message_id=5633, url=f'/',
                                   text='To main')


@app.route('/profile/avatar/<int:user_id>')
@login_required
def profile_avatar(user_id):
    img = Img.query.filter_by(user_id=user_id).first()
    if not img:
        return 'NO IMG', 404
    return Response(img.img, mimetype=img.mimetype)


@app.route('/profile/avatar/upload/<int:user_id>', methods=['POST', 'GET'])
@login_required
def profile_avatar_upload(user_id):
    if request.method == 'POST':

        pic = request.files['pic']
        if not pic:
            return render_template('profile_avatar_upload.html', no_file=True)
        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype
        if not filename or not mimetype:
            return render_template('profile_avatar_upload.html', err_file=True)
        img = Img.query.filter_by(user_id=user_id).first()
        try:
            if not img:
                img = Img(user_id=user_id, img=pic.read(), name=filename, mimetype=mimetype)
                db.session.add(img)
                db.session.commit()
            else:
                img.img = pic.read()
                img.name = filename
                img.mimetype = mimetype
                db.session.commit()
        except Exception as e:
            print(e)
            return render_template('notification.html', message=MESSAGE_LIST[4898], message_id=4898,
                                   url=f'/profile/{user_id}', text='Back')
        return render_template('notification.html', message=MESSAGE_LIST[1186], message_id=1186,
                               url=f'/profile/{user_id}', text='Back to profile')
    else:
        return render_template('profile_avatar_upload.html')


@app.route('/signin', methods=['POST', 'GET'])  # войти
def signin():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        fatname = request.form['fatname']
        password = request.form['password']

        if not all((name, surname, fatname, password)):
            return render_template('signin.html', clear_fields=True)

        user = Users.query.filter_by(name=name, fatname=fatname, surname=surname).first()
        if user:
            if check_password_hash(user.password, password):
                userlogin = UserLogin().create(user)
                login_user(userlogin)
                return redirect(f'/profile/{user.user_id}')
        else:
            return render_template('signin.html', err_data=True)

    return render_template('signin.html')


@app.route('/signup', methods=['POST', 'GET'])  # зарегаться
def signup():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        fatname = request.form['fatname']

        password_1 = request.form['password_1']
        password_2 = request.form['password_2']
        type_user = request.form.get('type_user')
        is_teacher = True if type_user == 'teacher' else False
        is_student = not is_teacher
        if password_1 != password_2:
            return render_template('signup.html', password_mismatch=True)
        if not all((name, surname, fatname, password_1, password_2, type_user)):
            return render_template('signup.html', clear_fields=True)
        if Users.query.filter_by(name=name, fatname=fatname, surname=surname).first():
            return render_template('signup.html', user_exists=True)
        password = generate_password_hash(password_1)
        user = Users(name=name, surname=surname, fatname=fatname, password=password, is_teacher=is_teacher,
                     is_student=is_student)
        try:
            db.session.add(user)
            db.session.commit()

            return render_template('notification.html', message=MESSAGE_LIST[1237], message_id=1237, url='/',
                                   text='To main')
        except:
            return render_template('notification.html', message=MESSAGE_LIST[4898], message_id=4898, url='/signup',
                                   text='Back')
    else:
        return render_template('signup.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
