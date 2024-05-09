from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required
from UserLogin import UserLogin
from flask import Flask, request, render_template, Response
from werkzeug.utils import secure_filename
from db import db_init, db
from models import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db_init(app)

login_manager = LoginManager(app)


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


@app.route('/singin')  # войти
def profile(user_id):
    pass


@app.route('/singup>')  # зарегаться
def profile(user_id):
    pass


# только для учителя
@app.route('myclass/<int:user_id>')  # все классы учителя
def foo(user_id):
    pass


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
