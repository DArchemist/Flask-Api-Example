import json
from api.utils.test_base import BaseTestCase
from api.models.users import User
from datetime import datetime
import unittest2 as unittest
from api.utils.token import generate_verification_token, confirm_verification_token

def create_users():
    user1 = User(email="darleyortiz@hotmail.com", username="DArchemist3", password=User.generate_hash('helloworld'), isverified=True).create()
    user2 = User(email="darleyortizz@hotmail.com", username="DArchemist4", password=User.generate_hash('helloworld')).create()


class TestUsers(BaseTestCase):
    def setUp(self):
        super(TestUsers, self).setUp()
        create_users()

    def test_login_user(self):
        user = {
            "email": "darleyortiz@hotmail.com",
            "password": "helloworld"
        }
        response = self.app.post(
            '/api/users/login',
            data=json.dumps(user),
            content_type='application/json'
        )
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue('access_token' in data)

    def test_login_user_wrong_credentials(self):
        user = {
        "email": "darleyortiz@hotmail.com",
        "password": "helloworld12"
        }
        response = self.app.post('/api/users/login',
        data=json.dumps(user),
        content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(401, response.status_code)

    def test_login_unverified_user(self):
        user = {
        "email": "darleyortizz@hotmail.com",
        "password": "helloworld"
        }
        response = self.app.post('/api/users/login',
        data=json.dumps(user),
        content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(400, response.status_code)

    def test_create_user(self):
        user = {
        "username": "nicoCaos",
        "password": "1234567891011",
        "email": "andresortizchemist@gmail.com"
        }
        response = self.app.post('/api/users/',
        data=json.dumps(user),
        content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(201, response.status_code)
        self.assertTrue('success' in data['code'])

    def test_create_user_without_username(self):
        user = {
        "password": "helloworld",
        "email": "testemail@gmail.com"
        }
        response = self.app.post('/api/users/',
        data=json.dumps(user),
        content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(422, response.status_code)

    def test_confirm_email(self):
        token = generate_verification_token('darleyortizz@hotmail.com')
        response = self.app.get('/api/users/confirm/'+token)
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue('success' in data['code'])

    def test_confirm_email_for_verified_user(self):
        token = generate_verification_token('darleyortiz@hotmail.com')
        response = self.app.get('/api/users/confirm/'+token)
        data = json.loads(response.data)
        self.assertEqual(422, response.status_code)

    def test_confirm_email_with_incorrect_email(self):
        token = generate_verification_token('darleyortizsz@hotmail.com')
        response = self.app.get('/api/users/confirm/'+token)
        data = json.loads(response.data)
        self.assertEqual(404, response.status_code)




if __name__ == '__main__':
    unittest.main()
