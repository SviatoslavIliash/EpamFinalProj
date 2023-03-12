"""RESTful for app"""
import json

import flask_migrate
from flask import jsonify, request
from flask_httpauth import HTTPBasicAuth

from flask import render_template, url_for, request, flash, redirect, Blueprint, g
from flask_login import login_required, current_user, logout_user

from bikerepair.service.db_crud import create_user, check_login_user,\
    total_user_orders, create_user_order, \
    date_filter_orders, crud_status

bp = Blueprint('bp_api', __name__)

from bikerepair import db, login_manager, migrate
from bikerepair.models.models import User, Order, Service

auth = HTTPBasicAuth()


# configure login_manager
@login_manager.user_loader
def load_user(user_id):
    """Redefining load_user method for flask login"""
    return User.query.get(user_id)


@bp.route('/api/create_db')
def create_database():
    """Creating database and default service table"""
    try:
        flask_migrate.upgrade()
        Service.default_table(db)
        create_user('admin', '1234', '1234', 'admin@admin.com')
    except Exception:
        return jsonify(message='Database was already created'), 500
    return jsonify(message='Database successfully created'), 200


@bp.route('/api/create_db_no_migrations')
def create_database_no_migrations():
    """Creating database and default service table when no migrations folder"""
    try:
        flask_migrate.init()
        flask_migrate.migrate()
        flask_migrate.upgrade()
        Service.default_table(db)
        create_user('admin', '1234', '1234', 'admin@admin.com')
    except Exception:
        return jsonify(message='Database was already created'), 500
    return jsonify(message='Database successfully created'), 200

@auth.verify_password
def verify_password(my_login, password):
    """Verify password"""
    response = check_login_user(login=my_login, password=password)
    if response is None:
        return True

    return False


@bp.route('/api/signup', methods=['POST'])
def signup():
    """Api for logout function"""
    my_login = request.json.get('login')
    password = request.json.get('password')
    password2 = request.json.get('password2')
    email = request.json.get('email')

    response = create_user(login=my_login, password=password, password2=password2, email=email)

    if response is None:
        return jsonify(message=f'Registered {my_login}'), 201

    return jsonify(message=response), 400


@bp.route('/api/user_account/new_order', methods=['POST'])
@auth.login_required
def new_order():
    """Api for user account"""
    serv1 = request.json.get('wash')
    serv2 = request.json.get('repair')
    serv3 = request.json.get('upgrade')
    serv4 = request.json.get('lube_chain')
    services = [serv1, serv2, serv3, serv4]

    response = create_user_order(name=current_user.login, services=services)
    if response is not None:
        return jsonify(message=response), 400

    return jsonify(message='New order created'), 200


@bp.route('/api/user_account/user_orders', methods=['GET'])
@auth.login_required
def user_orders():
    """Api for user orders"""
    orders = total_user_orders(current_user.login)
    if len(orders) != 0:
        api_orders = []
        for order in orders:
            api_orders.append(str(order))
        return jsonify(api_orders), 200
    return jsonify(message='No orders yet'), 200


@bp.route('/api/admin_account/crud_orders', methods=['POST'])
@auth.login_required
def crud_orders():
    """Api for admin crud orders"""
    if current_user.login != 'admin':
        return jsonify(message='Access restricted'), 403

    change_status = request.json.get('status')
    delete_status = request.json.get('delete')
    current_id = request.json.get('current_id')

    current_order = Order.query.filter_by(id=current_id).first()
    if current_order:
        if crud_status(current_status=current_order.status, change_status=change_status,
                       delete_status=delete_status, current_id=current_id) is None:
            return jsonify(message='Order changed'), 200
        return jsonify(message='Internal server error'), 500
    return jsonify(message='Could not find such order'), 404


@bp.route('/api/admin_account/user_names', methods=['GET'])
@auth.login_required
def admin_user_names():
    """Api for admin, receive users with orders if True or all users"""
    if current_user.login != 'admin':
        return jsonify(message='Access restricted'), 403
    got_orders = request.args.get('got_orders')
    users = []

    if got_orders == 'True':
        users_with_order = db.session.query(Order.login).distinct()
        for user in users_with_order:
            users.append(user.login)
    else:
        users_all = db.session.query(User.login)
        for user in users_all:
            users.append(user.login)

    if len(users) != 0:
        return jsonify(users), 200

    return jsonify(message='No users yet'), 200


@bp.route('/api/admin_account/user_orders', methods=['GET'])
@auth.login_required
def admin_user_orders():
    """Api for admin, receive users and their orders. User splits by ", " """
    if current_user.login != 'admin':
        return jsonify(message='Access restricted'), 403

    wanted_user = request.args.get('user')
    users = ''
    check_users = ''
    if wanted_user:
        users = wanted_user.split(", ")
        check_users = [check for check in db.session.query(User).
                        filter(User.login.in_(users)) if check is not None]

    if len(users) != len(check_users):
        return jsonify(message='Bad request parameters!')

    total_order_output = []

    requested_users = users
    if not requested_users:
        requested_users = [user.login for user in db.session.query(User.login)]
    for user in requested_users:
        total_order_output.append(user)
        orders = total_user_orders(user)
        for order in orders:
            total_order_output.append(str(order))

    if len(total_order_output) != 0:
        return jsonify(total_order_output), 200

    return jsonify(message='No users yet'), 200


@bp.route('/api/admin_account/filter_orders', methods=['GET'])
@auth.login_required
def filter_orders():
    """Api for admin filter orders"""
    if current_user.login != 'admin':
        return jsonify(message='Access restricted'), 403
    date_first = request.args.get('date_first')
    date_second = str(request.args.get('date_second')) + ' 23:59:59'
    # added hours:minutes:seconds to take orders in current date

    admin_filter_orders = date_filter_orders(first=date_first, second=date_second)
    api_orders = []
    for order in admin_filter_orders:
        api_orders.append(str(order))

    if len(api_orders) != 0:
        return jsonify(api_orders), 200

    return jsonify(message='No orders yet'), 200
