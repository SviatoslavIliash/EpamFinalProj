# Database models
from flask_login import UserMixin
from sqlalchemy import func

from bikerepair import db

# Model for user
class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.login

    def get_id(self):
        return self.user_id

# Model for providing services
class Service(db.Model):
    name = db.Column(db.String(50), primary_key=True, unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    @staticmethod
    def default_table(current_db):
        current_db.session.add_all([
            Service(name='wash', price='50'),
            Service(name='repair', price='100'),
            Service(name='upgrade', price='150'),
            Service(name='lube_chain', price='50')
        ])
        current_db.session.commit()

    def __repr__(self):
        return '<Service %r>' % self.servname

# Model for client final order
class Order(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(50), db.ForeignKey('user.login'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, server_default=func.now())
    status = db.Column(db.Enum('pending', 'in process', 'done'), default='pending', nullable=False)
    services = ''
    total_price = 0

    def __repr__(self):
        return '<Order %r>' % self.id

# Model for few services in one order
class OrderItem(db.Model):
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), primary_key=True, nullable=False)
    serv_name = db.Column(db.String(50),
                          db.ForeignKey('service.name'),
                          primary_key=True,
                          nullable=False)
    price = db.Column(db.Integer, nullable=False)
