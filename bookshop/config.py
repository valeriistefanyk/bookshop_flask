class BaseConfig:
    pass

class DevConfig(BaseConfig):
    pass

class TestConfig(BaseConfig):
    TESTING = True

class ProdConfig(BaseConfig):
    DUBUG = False

configuration = {
    'dev': DevConfig,
    'test': TestConfig,
    'prod': ProdConfig,
}