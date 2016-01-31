class DevelopmentConfig(object):
    DATABASE_URI = "postgresql://wilbertabreu@localhost:5432/(projectname)"
    DEBUG = True

class TestingConfig(object):
    DATABASE_URI = "postgresql://wilbertabreu@localhost:5432/(projectname)-test"
    DEBUG = True
