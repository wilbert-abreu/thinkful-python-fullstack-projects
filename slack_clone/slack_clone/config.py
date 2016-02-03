class DevelopmentConfig(object):
    DATABASE_URI = "postgresql://wilbertabreu@localhost:5432/slack_clone"
    DEBUG = True

class TestingConfig(object):
    DATABASE_URI = "postgresql://wilbertabreu@localhost:5432/slack_clone-test"
    DEBUG = True
