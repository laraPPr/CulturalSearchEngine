import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'postgresql://[username]:[password]@[path]'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OBJECTS_PER_PAGE = 5
    ELASTICSEARCH_URL = 'http://localhost:9200'
