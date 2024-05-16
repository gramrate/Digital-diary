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
from variables import MESSAGE_LIST, BACK_LIST
from functions import check_name_into_database
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db_init(app)

login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    print('load_user')
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
    pass


@app.route('/singin', methods=['POST', 'GET'])  # войти
def singin():
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
        print(type_user)
        is_teacher = True if type_user == 'teacher' else False
        is_student = not is_teacher
        if password_1 != password_2:
            return render_template('singup.html', password_mismatch=True)
        if not all((name, surname, fatname, password_1, password_2, type_user)):
            return render_template('singup.html', clear_fields=True)

        all_users = Users.query.all()

        user_exists = check_name_into_database(name=name, surname=surname, fatname=fatname, all_users=all_users)

        if not user_exists:
            password = generate_password_hash(password_1)
            print(password)
            user = Users(name=name, surname=surname, fatname=fatname, password=password, is_teacher=is_teacher,
                         is_student=is_student)
            try:
                db.session.add(user)
                db.session.commit()
                return redirect('/notification/6640/1237')
            except Exception as e:
                raise e
                return redirect('/notification/3583/4898')
        else:
            return redirect('/notification/3583/1501')
    else:
        return render_template('singup.html')


# только для учителя
@app.route('/myclass/<int:user_id>')  # все классы учителя
def myclass(user_id):
    pass


@app.route('/notification/<int:back_id>/<int:message_id>')
def notification(back_id, message_id):
    message = MESSAGE_LIST.get(message_id)
    back = BACK_LIST.get(back_id)
    return render_template('notification.html', back=back, message=message, message_id=message_id)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
