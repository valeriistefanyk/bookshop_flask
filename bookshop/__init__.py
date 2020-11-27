from flask import Flask
from bookshop.config import configuration


def create_app(environment_name='dev'):
    app = Flask(__name__)
    app.config.from_object(configuration[environment_name])

    @app.route('/')
    def index():
        return '<h1>INDEX PAGE</h1>'

    return app