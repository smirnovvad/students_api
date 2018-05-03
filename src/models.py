
from flask_sqlalchemy import SQLAlchemy
# from crud import app


db = SQLAlchemy()


class Group(db.Model):
    __tablename__ = 'all_group'
    id = db.Column(db.Integer, primary_key=True)
    name_group = db.Column(db.String(50))



class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(50), unique=False)
    first_name = db.Column(db.String(20), unique=False)
    middle_name = db.Column(db.String(50), unique=False)
    email = db.Column(db.String(50), unique=True)
    phone = db.Column(db.String(11), unique=True)
    group_id = db.Column(db.Integer, db.ForeignKey('all_group.id'))
    group = db.relationship('Group', uselist=False, lazy='select')
    traing = db.Column(db.String(12), unique=False)
    telegram_id = db.Column(db.String(40), unique=True)


    def __init__(self, email, first_name, last_name, middle_name, group_id, traing, telegram_id, phone):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.middle_name = middle_name
        self.group_id = group_id
        self.traing = traing
        self.telegram_id = telegram_id
        self.phone = phone


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(50), unique=False)
    first_name = db.Column(db.String(20), unique=False)
    middle_name = db.Column(db.String(50), unique=False)
    email = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(50), unique=True)
    telegram_id = db.Column(db.String(40), unique=True)
