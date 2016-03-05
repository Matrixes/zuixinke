#-*- coding:utf-8 -*-
import os

DB_URL = os.environ.get('DB_URL')

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or ''

    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    MAIL_SUBJECT_PREFIX = u'醉心客'
    MAIL_SENDER = os.environ.get('MAIL_USERNAME')

    POSTS_PER_PAGE = 5

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = DB_URL + 'min'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = DB_URL + 'test'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = DB_URL + 'pro'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}