from db import db


class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    surname = db.Column(db.String(20), nullable=False)
    fatname = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    is_teacher = db.Column(db.Boolean, default=False)
    is_student = db.Column(db.Boolean, default=False)


class Img(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True)
    img = db.Column(db.Text, unique=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True)
    class_num = db.Column(db.String(3), nullable=False)
    class_let = db.Column(db.String(3), nullable=False)


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True)
    teacher_classes = db.Column(db.String(70), nullable=False, default='[]')
    subject_id = db.Column(db.Integer)


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True)
    subject_id = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    date = db.Column(db.String(20), nullable=False)
    comment = db.Column(db.String(50), nullable=False)


class Subjucts(db.Model):
    subject_id = db.Column(db.Integer, primary_key=True)
    subject_name = db.Column(db.String(30), nullable=False)
