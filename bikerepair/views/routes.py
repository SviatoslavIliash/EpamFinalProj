"""Flask routes for application"""
from flask import render_template, url_for, request, flash, redirect, Blueprint
from flask_login import login_required, current_user, logout_user

from bikerepair.service.db_crud import create_user, check_login_user, total_user_orders, create_user_order, \
    date_filter_orders, crud_status

bp = Blueprint('bp', __name__)

from bikerepair import db, login_manager
from bikerepair.models.models import User, Order


@login_manager.user_loader  # configure login_manager
def load_user(user_id):
    """Redefining load_user method for flask login"""
    return User.query.get(user_id)


@bp.route('/', methods=['GET'])  # route for home page
@bp.route('/home', methods=['GET'])
def index():
    """Route for main page"""
    return render_template("index.html")


@bp.route('/login', methods=['GET', 'POST'])  # route for login page
def login():
    """Route for login page"""
    my_login = request.form.get('login')
    password = request.form.get('password')
    if request.method == 'POST':
        response = check_login_user(login=my_login, password=password)
        if response is None:
            next_page = url_for('bp.user', name=my_login)
            if my_login == 'admin':
                next_page = '/admin_account'
            return redirect(next_page)
        flash(response)
    return render_template('login.html')


@bp.route('/logout')  # route for logout function
@login_required
def logout():
    """Route for logout"""
    logout_user()
    flash("You have been logged out, my friend!")
    return redirect(url_for('bp.login'))


@bp.route('/signup', methods=['GET', 'POST'])  # route for signup page
def signup():
    """Route for sign up page"""
    my_login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    email = request.form.get('email')
    if request.method == 'POST':
        response = create_user(login=my_login, password=password, password2=password2, email=email)

        if response is None:
            return redirect(url_for('bp.login'))

        flash(response)

    return render_template("signup.html")


@bp.route('/user_account/<string:name>', methods=['GET', 'POST']) # route for user account
@login_required
def user(name):
    """Route for user account page"""
    serv1 = request.form.get('wash')
    serv2 = request.form.get('repair')
    serv3 = request.form.get('upgrade')
    serv4 = request.form.get('lube_chain')
    services = [serv1, serv2, serv3, serv4]
    if request.method == 'POST':
        response = create_user_order(name=name, services=services)
        if response is not None:
            flash(response)

    if current_user.login == name:
        return render_template('user_account.html', name=name, user_orders=total_user_orders(name))

    flash('Log in required!!!')
    return redirect(url_for('bp.login'))


@bp.route('/admin_account', methods=['GET', 'POST'])  # route for admin account
@login_required
def admin():
    """Route for admin account page"""
    current_status = request.form.get('current_status')
    change_status = request.form.get('status')
    delete_status = request.form.get('delete')
    current_id = request.form.get('current_id')
    order_date_first = request.args.get('order_date_first')
    order_date_second = str(request.args.get('order_date_second')) + ' 23:59:59'
    # added hours:minutes:seconds to take orders in current date
    users = db.session.query(Order.login).distinct()

    if request.method == 'POST':
        crud_status(current_status=current_status, change_status=change_status,
                    delete_status=delete_status, current_id=current_id)

    filter_orders = date_filter_orders(first=order_date_first, second=order_date_second)

    if current_user.login == 'admin':
        return render_template('admin.html',
                               users=users,
                               total_user_orders=total_user_orders,
                               filter_orders=filter_orders)

    flash('Log in required!!!')
    return redirect(url_for('bp.login'))
