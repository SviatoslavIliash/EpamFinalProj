from flask_login import UserMixin, login_manager

from app import db


class User(db.Model, UserMixin):
    #user_id = db.Column(db.Integer, autoincrement=True)
    login = db.Column(db.String(50), primary_key=True, unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.login


class Service(db.Model):
    #id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    servname = db.Column(db.String(50), primary_key=True, unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Service %r>' % self.id


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(50), unique=True, nullable=False)
    servname = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Order %r>' % self.id


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)
