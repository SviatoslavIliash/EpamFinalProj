"""Init file for application"""
import os
import configparser
import logging

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


def read_config(section_name):
    """Reading config file"""
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini'))
    db_type = config[section_name]['DBtype']
    # db_ is name for mysql and path to file for sqlite
    db_ = ''
    if config.has_option(section_name, 'Database'):
        db_ = config[section_name]['Database']
    uri = ''
    if db_type == 'mysql':
        username = config[section_name]['UserName']
        password = config[section_name]['Password']
        host = config[section_name]['Host']
        uri = f'{db_type}+pymysql://{username}:{password}@{host}/{db_}'
    else:
        if db_ == "":
            uri = 'sqlite://'
        else:
            uri = f'sqlite:////{db_}'
    return uri


logger = logging.getLogger()  # create root logger
logFormatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
# add console handler to the root logger
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)

# add file handler to the root logger
fileHandler = logging.FileHandler('bikerepair.log')
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


# creating Flask application
def create_app(section_name='DEVELOP'):
    """App factory"""
    app = Flask(__name__)
    from bikerepair.views.routes import bp
    from bikerepair.rest.api_routes import bp as bp_api
    app.register_blueprint(bp_api)
    app.register_blueprint(bp)
    app.secret_key = 'some secret key'
    app.config['SQLALCHEMY_DATABASE_URI'] = read_config(section_name)
    app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

    db.init_app(app)
    migrate.init_app(app, db, directory=os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'migrations'))
    # init Flask login manager

    login_manager.init_app(app)
    login_manager.login_view = 'bp.login'

    return app

from bikerepair.views import routes
