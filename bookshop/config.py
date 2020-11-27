class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
    SQLALCHEMY_ECHO = True

class TestConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    TESTING = True

class ProdConfig(BaseConfig):
    DUBUG = False

configuration = {
    'dev': DevConfig,
    'test': TestConfig,
    'prod': ProdConfig,
}