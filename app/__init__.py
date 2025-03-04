import logging

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

from app import routes, models, errors

if not app.debug:
    if not os.path.exists('logs'):
        os.makedirs('logs')
    file_handler = RotatingFileHandler('logs/solana-market.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('App started')