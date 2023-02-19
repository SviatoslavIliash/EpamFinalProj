from flask import Flask, render_template, url_for, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from re import match
from flask_login import login_user, LoginManager, login_required, UserMixin, current_user, logout_user
#from config import db_config
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.secret_key = 'some secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:2570947K!@localhost/bikerepair'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

#from flask_login import UserMixin, login_manager




class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.login

    def get_id(self):
        return self.user_id

class Service(db.Model):
    #id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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

### Filing Service table

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(50), db.ForeignKey('user.login'), nullable=False)
    #servname = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)


    def __repr__(self):
        return '<Order %r>' % self.id


class OrderItem(db.Model):
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), primary_key=True, nullable=False)
    serv_name = db.Column(db.String(50), db.ForeignKey('service.name'), primary_key=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)


with app.app_context():
    db.create_all()
    #Service.default_table(db)


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

                #next_page = request.form.get('/user/<string:login>')
                next = f'user_account/{login}'
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


@app.route('/user_account/<string:name>', methods=['GET', 'POST'])
@login_required
def user(name):
    serv1 = request.form.get('wash')
    serv2 = request.form.get('repair')
    serv3 = request.form.get('upgrade')
    serv4 = request.form.get('lube_chain')
    services = [serv1, serv2, serv3, serv4]
    if request.method == 'POST':
        order = Order(login=name, status='pending')
        db.session.add(order)
        db.session.flush()
        for service in services:
            if service:
                order_item = OrderItem(order_id=order.id, serv_name=service,
                                    price=db.session.query(Service.price).filter(Service.name==service))
                db.session.add(order_item)
            db.session.commit()

    user_orders = Order.query.filter_by(login=name)
    order_list =[]
    for i in user_orders:
        order_list.append(i)

    if current_user.login == name:
        return render_template('user_account.html', name=name, user_orders=order_list)
    else:
        flash('Log in required!!!')
        return redirect(url_for('login'))


@app.route('/admin_account', methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.login == 'admin':
        return render_template('admin.html')
    else:
        flash('Log in required!!!')
        return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
