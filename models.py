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
    name = db.Column(db.String(50), primary_key=True, unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Service %r>' % self.servname


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(50), db.ForeignKey('user.login'), nullable=False)
    #servname = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)


    def __repr__(self):
        return '<Order %r>' % self.id


class OrderItem(db.Moder):
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'),  nullable=False)
    serv_name = db.Column(db.String(50), db.ForeignKey('service.name'), nullable=False)
    price = db.Column(db.Integer, nullable=False)


#@login_manager.user_loader
#def load_user(user_id):
#    return User.get(user_id)
