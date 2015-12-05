import os

class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://ubuntu:wilbertabreu@locahost:5432/blogful"
    DEBUG = True
