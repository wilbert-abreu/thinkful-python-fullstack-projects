import os

class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://wilbertabreu@localhost:5432/blogful"
    DEBUG = True
