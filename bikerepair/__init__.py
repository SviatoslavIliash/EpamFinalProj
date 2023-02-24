from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = 'some secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:2570947K!@localhost/bikerepair'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)


from bikerepair import routes
