from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
#from config import db_config


app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:2570947K!@localhost/bikerepair'
#app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
#db = SQLAlchemy(app)


@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def index():
    return render_template("index.html")


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/signup')
def signup():
    return render_template("signup.html")


@app.route('/user/<string:name>')
def user(name):
    return "Hello " + name


if __name__ == "__main__":
    app.run(debug=True)
