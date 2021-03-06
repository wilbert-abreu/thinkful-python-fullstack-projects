class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = "postgresql://wilbertabreu@localhost:5432/blogful"
    SECRET_KEY = "my_secret_key_here"
    DEBUG = True

class TestingConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://wilbertabreu@localhost:5432/blogful-test"
    SECRET_KEY = "Not secret"
    DEBUG = False

class TravisConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost:5432/blogful-test"
    DEBUG = False
    SECRET_KEY = "Not secret"