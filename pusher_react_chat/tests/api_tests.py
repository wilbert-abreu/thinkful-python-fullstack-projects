import unittest
import os
try: from urllib.parse import urlparse
except ImportError: from urlparse import urlparse # Py2 compatibility
import sys; print(list(sys.modules.keys()))


# Configure our app to use the testing databse
os.environ["CONFIG_PATH"] = "realtime_chat.config.TestingConfig"

from realtime_chat import app
from realtime_chat import models
from realtime_chat.database import Base, engine, session

class TestAPI(unittest.TestCase):
    """ Tests for the tuneful API """

    def setUp(self):
        """ Test setup """
        self.client = app.test_client()

        # Set up the tables in the database
        Base.metadata.create_all(engine)


    def tearDown(self):
        """ Test teardown """
        session.close()
        # Remove the tables and their data from the database
        Base.metadata.drop_all(engine)



