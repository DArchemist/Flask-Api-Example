import unittest2 as unittest
from main import create_app
from api.utils.database import db
from api.config.config import TestingConfig
import tempfile

class BaseTestCase(unittest.TestCase):
    """A base test case"""
    def setUp(self):
        app = create_app(TestingConfig)
        self.test_db_file = tempfile.mkstemp()[1]
        app.config['DATABASE'] = self.test_db_file
        db.init_app(app)
        with app.app_context():
            db.create_all()
        app.app_context().push()
        self.app = app.test_client()
    def tearDown(self):
        db.drop_all()
