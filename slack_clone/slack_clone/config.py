class DevelopmentConfig(object):
    DATABASE_URI = "postgresql://wilbertabreu@localhost:5432/slack_clone"
    SECRET_KEY = "my_secret_key_here"
    DEBUG = True

class TestingConfig(object):
    DATABASE_URI = "postgresql://wilbertabreu@localhost:5432/slack_clone-test"
    SECRET_KEY = "my_secret_key_here"
    DEBUG = True
