from flask import Flask, render_template

from bookshop.config import configuration
from bookshop.extenstions import db, csrf
from bookshop.blueprints.books import books


def create_app(environment_name='dev'):
    app = Flask(__name__)
    app.config.from_object(configuration[environment_name])

    db.init_app(app)
    csrf.init_app(app)
    
    @app.route('/')
    def index():
        return render_template('home/index.html')

    app.register_blueprint(books, url_prefix='/books')


    @app.errorhandler(404)
    def not_found(exception):
        return render_template('404.html'), 404

    return app