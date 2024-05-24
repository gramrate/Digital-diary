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
from functions import get_user_by_name

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


@app.route('/diary/<int:user_id>')  # расписание
def diary(user_id):
    pass


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
