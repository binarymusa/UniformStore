
""" contains links to database connections, mail client.
    ie.,mysql
    ie.gmail, yahoo,
    also holds the secret key used in form validations
"""
import os
# from os import environ
# from dotenv import load_dotenv

# Load environment variables from .env file
# load_dotenv()

class Config:
    """ SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key')
    DB_USERNAME = os.environ.get('DB_USERNAME', 'default_username')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'default_password')
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_NAME = os.environ.get('DB_NAME', 'Automobile')

    print("DB_USERNAME:", repr(DB_USERNAME))
    print("DB_PASSWORD:", repr(DB_PASSWORD))


    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{(DB_USERNAME)}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True """

    SECRET_KEY = '297f539cb5b687dfb8021b30'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://MUSTAFA:5m9l<18>_X!@localhost/Uniform'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    MAIL_SERVER = 'smtp.google.com'
    MAIL_PORT = 587    
    MAIL_USE_TLS = True
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')



""" unfinished """
# class DevelopmentConfig(Config):
#     DEBUG = True
#     SQLALCHEMY_DATABASE_URI = ''

# class TestingConfig(Config):
#     TESTING = True
#     SQLALCHEMY_DATABASE_URI = 'sqlite:/// data-test.sqlite'

# class ProductionConfig(Config):
#     SQLALCHEMY_DATABASE_URI = 'sqlite:/// data-test.sqlite'


# config = {
# 'development': DevelopmentConfig,
# 'testing': TestingConfig,
# 'production': ProductionConfig,
# 'default': DevelopmentConfig
# }