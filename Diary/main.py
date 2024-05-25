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
from variables import MESSAGE_LIST
from functions import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db_init(app)

login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id, Users)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/schedule/<date>/<int:user_id>')  # расписание
def diary(date, user_id):
    user = Users.query.filter_by(user_id=user_id).first()
    if not user:
        return render_template('notification.html', message=MESSAGE_LIST[5633], message_id=5633, url=f'/',
                               text='To main')

    if user.is_teacher:
        pass # сделать обработку на урок этого человека
    elif user.is_student:
        student = Student.query.filter_by(user_id=user_id).first()
        if len(date) != 8:
            date = get_time()
            err_date = True
        else:
            date = date[:2] + '/' + date[2:4] + '/' + date[4:]
            err_date = False
        day = Schedule.query.filter_by(date=date, class_num=student.class_num, class_let=student.class_let)
        next_day = add_one_day(date)
        next_day = add_one_day(date)
        prev_day = subtract_one_day(date)

        if day.count():
            subjects = Subjects.query.all()
            all_subjects = ['null']
            for subj in subjects:
                all_subjects.append(subj.subject_name)
            return render_template('schedule.html', user_id=user_id, day=day, all_subjects=all_subjects, date=date, err_date=err_date, next_day=next_day, prev_day=prev_day)
        else:
            return render_template('schedule.html', user_id=user_id, empty_day=True, date=date, next_day=next_day, prev_day=prev_day)


@app.route('/666')  # расписание
def sixsixsix():
    '''
    day = Schedule(class_num='10', class_let='A', subject_id=1, lesson_number=1, teacher_user_id=1, homework="Подготовить доклад", date='26/05/2024', weekday='sun')
    db.session.add(day)
    day = Schedule(class_num='10', class_let='A', subject_id=2, lesson_number=2, teacher_user_id=1, homework="Решить Задачи", date='26/05/2024', weekday='sun')
    db.session.add(day)
    day = Schedule(class_num='10', class_let='A', subject_id=1, lesson_number=3, teacher_user_id=1, homework="Не Задано", date='26/05/2024', weekday='sun')
    db.session.add(day)
    day = Schedule(class_num='10', class_let='A', subject_id=4, lesson_number=4, teacher_user_id=1, date='26/05/2024', weekday='sun')
    db.session.add(day)
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
    '''
    student = Student(user_id=2, class_num='11', class_let='A')
    db.session.add(student)
    db.session.commit()
    return 'True'
@app.route('/homeworks/<int:user_id>')  # ДЗ
def homeworks(user_id):
    pass


@app.route('/ratings/<int:user_id>')  # оценки
def ratings(user_id):
    pass


@app.route('/profile/<int:user_id>')  # Профиль
def profile(user_id):
    user = Users.query.filter_by(user_id=user_id).first()
    student = Student.query.filter_by(user_id=user_id).first()
    if user:
        if not student:
            class_num = 'You haven\'t been assigned to a class yet'
            class_let = ''
        else:
            class_num = student.class_num
            class_let = f'"{student.class_let}"'
        return render_template('profile.html', user_id=user_id, name=user.name, surname=user.surname,
                               fatname=user.fatname, is_student=user.is_student, is_teacher=user.is_teacher, class_num=class_num, class_let=class_let)
    else:
        return render_template('notification.html', message=MESSAGE_LIST[5633], message_id=5633, url=f'/',
                               text='To main')


@app.route('/profile/edit/<int:user_id>', methods=['POST', 'GET'])  # Профиль
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
            return render_template('profile_edit.html', clear_fields=True)

        try:
            user.name=name
            user.surname=surname
            user.fatname=fatname
            user.is_student=is_student
            user.is_teacher=is_teacher
            db.session.commit()
            return render_template('notification.html', message=MESSAGE_LIST[3965], message_id=3965, url=f'/profile/{user_id}', text='Back to profile')
        except Exception as e:
            print(e)
            return render_template('notification.html', message=MESSAGE_LIST[4898], message_id=4898, url=f'/profile/{user_id}', text='Back to profile')

    else:
        if user:
            is_student = user.is_student
            is_teacher = user.is_teacher
            return render_template('profile_edit.html', user_id=user_id, name=user.name, surname=user.surname, fatname=user.fatname, is_student=is_student, is_teacher=is_teacher)
        else:
            return render_template('notification.html', message=MESSAGE_LIST[5633], message_id=5633, url=f'/',
                                   text='To main')


@app.route('/profile/avatar/<int:user_id>')
def profile_avatar(user_id):
    img = Img.query.filter_by(user_id=user_id).first()
    if not img:
        return 'NO IMG', 404
    return Response(img.img, mimetype=img.mimetype)


@app.route('/profile/avatar/upload/<int:user_id>', methods=['POST', 'GET'])
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
                img.img=pic.read()
                img.name=filename
                img.mimetype=mimetype
                db.session.commit()
        except Exception as e:
            print(e)
            return render_template('notification.html', message=MESSAGE_LIST[4898], message_id=4898, url=f'/profile/{user_id}', text='Back')
        return render_template('notification.html', message=MESSAGE_LIST[1186], message_id=1186, url=f'/profile/{user_id}', text='Back to profile')
    else:
        return render_template('profile_avatar_upload.html')


@app.route('/singin', methods=['POST', 'GET'])  # войти
def singin():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        fatname = request.form['fatname']
        password = request.form['password']

        if not all((name, surname, fatname, password)):
            return render_template('singin.html', clear_fields=True)

        all_users = Users.query.all()
        user = get_user_by_name(name, surname, fatname, all_users=all_users)
        if user:
            if check_password_hash(user.password, password):
                userlogin = UserLogin().create(user)
                login_user(userlogin)
                return redirect(f'/profile/{user.user_id}')
        else:
            return render_template('singin.html', err_data=True)

    return render_template('singin.html')


@app.route('/singup', methods=['POST', 'GET'])  # зарегаться
def singup():
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
            return render_template('singup.html', password_mismatch=True)
        if not all((name, surname, fatname, password_1, password_2, type_user)):
            return render_template('singup.html', clear_fields=True)


        password = generate_password_hash(password_1)
        user = Users(name=name, surname=surname, fatname=fatname, password=password, is_teacher=is_teacher,
                     is_student=is_student)
        try:
            db.session.add(user)
            db.session.commit()

            return render_template('notification.html', message=MESSAGE_LIST[1237], message_id=1237, url='/',
                                   text='To main')
        except:
            return render_template('notification.html', message=MESSAGE_LIST[4898], message_id=4898, url='/singup',
                                   text='Back')
    else:
        return render_template('singup.html')


# только для учителя
@app.route('/myclass/<int:user_id>')  # все классы учителя
def myclass(user_id):
    pass


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
