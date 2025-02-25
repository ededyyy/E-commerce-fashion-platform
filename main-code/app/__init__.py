from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
import logging
from logging.handlers import RotatingFileHandler
import os


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)


def configure_logging(app):
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    system_handler = RotatingFileHandler(
        os.path.join(log_dir, 'system.log'),
        maxBytes=1024 * 1024,
        backupCount=10
    )
    system_handler.setLevel(logging.INFO)
    system_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # noqa: E402, F401
    system_handler.setFormatter(system_formatter)

    user_handler = RotatingFileHandler(
        os.path.join(log_dir, 'user.log'),
        maxBytes=1024 * 1024,
        backupCount=10
    )
    user_handler.setLevel(logging.INFO)
    user_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # noqa: E402, F401
    user_handler.setFormatter(user_formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')  # noqa: E402, F401
    console_handler.setFormatter(console_formatter)

    app.logger.addHandler(system_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(logging.DEBUG)

    user_logger = logging.getLogger('user')
    user_logger.addHandler(user_handler)
    user_logger.addHandler(console_handler)
    user_logger.setLevel(logging.INFO)


configure_logging(app)

from app import views, models  # noqa: E402, F401