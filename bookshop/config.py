import os


class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    SECRET_KEY = os.getenv('SECRET_KEY', 'rand01013232')
    LANGUAGES = {
        'uk': 'Українська',
        'ru': 'Русский',
        'en': 'English',
    }

class DevConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
    SQLALCHEMY_ECHO = True

class TestConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    WTF_CSRF_ENABLED = False
    TESTING = True

class ProdConfig(BaseConfig):
    SECRET_KEY = os.getenv('SECRET_KEY')
    DUBUG = False


configuration = {
    'dev': DevConfig,
    'test': TestConfig,
    'prod': ProdConfig,
}
