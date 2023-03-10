"""Functions for checking user`s information
and CRUD orders"""
from re import match
from typing import Optional

from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user
from sqlalchemy import desc, func

from bikerepair import db
from bikerepair.models.models import User, Order, OrderItem, Service


# login user
def check_login_user(login, password) -> Optional[str]:
    """Check if users login is correct"""
    if not (login.strip() and password):
        return 'Please fill login and password fields'

    my_user = User.query.filter_by(login=login).first()

    if my_user and check_password_hash(my_user.password, password):
        login_user(my_user)
        return None

    return 'Login or password is not correct'


# total_user_function using by two routes Admin and User
def total_user_orders(name) -> list:
    """Collecting full user`s order
     and return list of all user`s orders"""
    user_orders = Order.query.filter_by(login=name).order_by(desc(Order.date))
    total_orders = []

    for user_order in user_orders:
        current_order = Order(id=user_order.id, login=name,
                              status=user_order.status, date=user_order.date)
        order_items = OrderItem.query.filter_by(order_id=user_order.id)
        price_sum = db.session.query(func.sum(OrderItem.price).label("total")).\
            filter_by(order_id=user_order.id).scalar()
        services = []
        for item in order_items:
            services.append(item.serv_name)

        current_order.services = ", ".join(services)
        current_order.total_price = price_sum
        total_orders.append(current_order)
    return total_orders


# create user
def create_user(login, password, password2, email) -> Optional[str]:
    """Creating user and validate information"""
    if not (login.strip() and password and password2 and email.strip()):
        return 'Please, fill all fields!'

    if not validate_login(login):
        return 'Login must be 3-40 length and contents only letters, numbers, underscore!'

    if password != password2:
        return 'Passwords are not equal!'

    if User.query.filter_by(login=login).first():
        return 'Such login exists. Choose another name!'

    hash_pwd = generate_password_hash(password)
    new_user = User(login=login, password=hash_pwd, email=email)
    db.session.add(new_user)
    db.session.commit()
    return None


# Check if login is valid according to requirements
def validate_login(login) -> bool:
    """ Check if login is valid"""
    if match(r"^[a-zA-Z0-9_]{3,40}$", login):
        return True
    return False


# user order for user account
def create_user_order(name, services) -> Optional[str]:
    """Create order and check if service exist"""
    service_choice = [serv for serv in services if serv is not None]
    if len(service_choice) == 0:
        return 'Choose service!'

    order = Order(login=name)
    db.session.add(order)
    db.session.flush()
    for service in service_choice:
        if service:
            order_item = OrderItem(order_id=order.id, serv_name=service,
                                   price=db.session.query(Service.price).filter(
                                       Service.name == service))
            db.session.add(order_item)
        db.session.commit()
    return None


# filter orders for admin
def date_filter_orders(first, second):
    """Filter orders by date"""
    filter_orders = db.session.query(Order).filter(Order.date.between(
        first, second))
    return filter_orders


# crud for orders in admin account
def crud_status(current_status, change_status, delete_status, current_id):
    """Change order status or delete order"""
    if delete_status:
        db.session.query(OrderItem).filter(OrderItem.order_id == current_id).delete()
        db.session.query(Order).filter(Order.id == current_id).delete()
        db.session.commit()
    else:
        if change_status != current_status:
            db.session.query(Order).filter(Order.id == current_id).update(
                    {Order.status: change_status})
            db.session.commit()
