from flask import Flask, render_template, request, session, redirect

from bookshop.config import configuration
from bookshop.extenstions import db, csrf, login_manager, babel
from bookshop.blueprints.books import books
from bookshop.blueprints.users import users


def create_app(environment_name='dev'):
    app = Flask(__name__)
    app.config.from_object(configuration[environment_name])

    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    babel.init_app(app)

    @app.context_processor
    def inject_conf_var():
        return dict(
                AVAILABLE_LANGUAGES=app.config['LANGUAGES'],
                CURRENT_LANGUAGE=session.get('language',request.accept_languages.best_match(app.config['LANGUAGES'].keys())))

    @babel.localeselector
    def get_locale():
        try:
            language = session['language']
        except KeyError:
            language = None
        if language is not None:
            return language
        return request.accept_languages.best_match(app.config['LANGUAGES'].keys())

    @app.route('/')
    def index():
        return render_template('home/index.html')

    @app.route('/language/<language>')
    def set_language(language=None):
        session['language'] = language
        return redirect('/')

    app.register_blueprint(books, url_prefix='/books')
    app.register_blueprint(users)

    @app.errorhandler(404)
    def not_found(exception):
        return render_template('404.html'), 404

    return app