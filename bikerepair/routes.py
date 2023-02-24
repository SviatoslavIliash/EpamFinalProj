from re import match

from flask import render_template, url_for, request, flash, redirect
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, LoginManager, login_required, current_user, logout_user
from sqlalchemy import desc


from bikerepair import app, db
from bikerepair.models import User, Order, OrderItem, Service


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def index():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    login = request.form.get('login')
    password = request.form.get('password')
    if request.method == 'POST':
        if login.strip() and password:
            user = User.query.filter_by(login=login).first()

            if user and check_password_hash(user.password, password):
                login_user(user)

                next = url_for('user', name=login)
                if login == 'admin':
                    next = '/admin_account'
                return redirect(next)
            else:
                flash('Login or password is not correct')
        else:
            flash('Please fill login and password fields')

    return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You have been logged out, my friend!")
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    email = request.form.get('email')
    if request.method == 'POST':
        if User.query.filter_by(login=login).first():
            flash('Such login exists. Choose another name!')
            return render_template("signup.html")
        if match(r"^[a-zA-Z0-9_]{3,40}$", login):
            if not (login.strip() and password and password2 and email.strip()):
                flash('Please, fill all fields!')
            elif password != password2:
                flash('Passwords are not equal!')
            else:
                hash_pwd = generate_password_hash(password)
                new_user = User(login=login, password=hash_pwd, email=email)
                db.session.add(new_user)
                db.session.commit()

            return redirect(url_for('login'))
        else:
            flash('Login must be 3-40 length and contents only letters, numbers, underscore!')
    return render_template("signup.html")


def total_user_orders(name):
    user_orders = Order.query.filter_by(login=name).order_by(desc(Order.date))
    total_orders = []

    for o in user_orders:
        current_order = Order(id=o.id, status=o.status, date=o.date)
        order_items = OrderItem.query.filter_by(order_id=o.id)
        services = []
        for item in order_items:
            services.append(item.serv_name)
            current_order.total_price += int(item.price)
        current_order.services = ", ".join(services)
        total_orders.append(current_order)
    return total_orders


@app.route('/user_account/<string:name>', methods=['GET', 'POST'])
@login_required
def user(name):
    serv1 = request.form.get('wash')
    serv2 = request.form.get('repair')
    serv3 = request.form.get('upgrade')
    serv4 = request.form.get('lube_chain')
    services = [serv1, serv2, serv3, serv4]
    if request.method == 'POST':
        if not(serv1 or serv2 or serv3 or serv4):
            flash('Choose service!')
            redirect(url_for('user', name=name))
        else:
            order = Order(login=name)
            db.session.add(order)
            db.session.flush()
            for service in services:
                if service:
                    order_item = OrderItem(order_id=order.id, serv_name=service,
                                        price=db.session.query(Service.price).filter(Service.name == service))
                    db.session.add(order_item)
                db.session.commit()

    if current_user.login == name:
        return render_template('user_account.html', name=name, user_orders=total_user_orders(name))
    else:
        flash('Log in required!!!')
        return redirect(url_for('login'))


@app.route('/admin_account', methods=['GET', 'POST'])
@login_required
def admin():
    current_status = request.form.get('current_status')
    change_status = request.form.get('status')
    delete_status = request.form.get('delete')
    current_id = request.form.get('current_id')
    order_date_first = request.form.get('order_date_first')
    order_date_second = str(request.form.get('order_date_second')) + ' 23:59:59'
    users = db.session.query(Order.login).distinct()
    filter_orders = []
    if request.method == 'POST':
        if delete_status:
            db.session.query(OrderItem).filter(OrderItem.order_id == current_id).delete()
            db.session.query(Order).filter(Order.id == current_id).delete()
            db.session.commit()
        else:
            if change_status != current_status:
                db.session.query(Order).filter(Order.id == current_id).update({Order.status:change_status})
                db.session.commit()

        filter_orders = db.session.query(Order).filter(Order.date.between(order_date_first, order_date_second))

    if current_user.login == 'admin':
        return render_template('admin.html', users=users, total_user_orders=total_user_orders, filter_orders=filter_orders)
    else:
        flash('Log in required!!!')
        return redirect(url_for('login'))