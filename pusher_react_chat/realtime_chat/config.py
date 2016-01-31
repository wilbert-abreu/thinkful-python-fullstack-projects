class DevelopmentConfig(object):
    DATABASE_URI = "postgresql://wilbertabreu@localhost:5432/realtime_chat"
    DEBUG = True

class TestingConfig(object):
    DATABASE_URI = "postgresql://wilbertabreu@localhost:5432/realtime_chat-test"
    DEBUG = True
