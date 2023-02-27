from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import configparser

# reading config file
config = configparser.ConfigParser()
config.read('bikerepair/config.ini')
username = config['DEFAULT']['UserName']
password = config['DEFAULT']['Password']
host = config['DEFAULT']['Host']
db_name = config['DEFAULT']['Database']

# creating Flask application
app = Flask(__name__)
app.secret_key = 'some secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{username}:{password}@{host}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)


from bikerepair import routes
