from flask import Flask

from bookshop.config import configuration
from bookshop.extenstions import db


def create_app(environment_name='dev'):
    app = Flask(__name__)
    app.config.from_object(configuration[environment_name])

    db.init_app(app)

    @app.route('/')
    def index():
        return '<h1>INDEX PAGE</h1>'

    return app