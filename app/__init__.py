# coding: utf-8

from flask import Flask
from os import path
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_babel import Babel
from config import config
from werkzeug.routing import BaseConverter


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


basedir = path.abspath(path.dirname(__file__))
print basedir
db = SQLAlchemy()
bootstrap = Bootstrap()
babel = Babel()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name='default'):
    app = Flask(__name__)
    app.url_map.converters['regex'] = RegexConverter
    print app.url_map.converters
    app.config.from_object(config[config_name])
    db.init_app(app)
    bootstrap.init_app(app)
    babel.init_app(app)
    login_manager.init_app(app)

    from auth import testhome as auth_blueprint
    app.register_blueprint(auth_blueprint)
    print db
    return app