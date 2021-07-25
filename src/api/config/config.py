class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'
    UPLOAD_FOLDER= 'images'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost:3306/production'
    SECRET_KEY = 'arantxacastilladelamancha'
    SECURITY_PASSWORD_SALT = 'arantxacastilladelamancha'


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost:3306/development'
    SQLALCHEMY_ECHO = False
    SECRET_KEY = 'themacarena'
    SECURITY_PASSWORD_SALT = 'themacarena'



class TestingConfig(Config):
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost:3306/testing'
    SQLALCHEMY_ECHO = False
    SECRET_KEY = 'dragvulcano'
    SECURITY_PASSWORD_SALT = 'dragvulcano'
