from flask import Flask, render_template

from bookshop.config import configuration
from bookshop.extenstions import db


def create_app(environment_name='dev'):
    app = Flask(__name__)
    app.config.from_object(configuration[environment_name])

    db.init_app(app)

    @app.route('/')
    def index():
        return render_template('home/index.html')

    @app.route('/books')
    def index_books():
        return render_template('books/index.html')

    @app.errorhandler(404)
    def not_found(exception):
        return render_template('404.html'), 404

    return app