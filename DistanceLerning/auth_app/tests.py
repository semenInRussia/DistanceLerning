from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from DistanceLerning.settings import VERSION

# Create your tests here.
User = get_user_model()


class AuthTestCase(TestCase):
    username: str = 'tester'
    password: str = "1234567f"
    email: str = "tester@email.com"

    def setUp(self) -> None:
        self.c = Client(HTTP_USER_AGENT='Mozilla/5.0')

        self.c.post(f'/api/{VERSION}/auth/', data={
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'role': 'teacher',
            'subject': 1,
        })

    def test_login(self):
        self.c.post(f'/api/{VERSION}/auth/', data={
            'username': self.username,
            'password': self.password
        })

        user = self.c.user

        self.assertEquals(user.username, self.username)

# {"username": "tester", "email": "tester@email.com", "password": "1234567f","role": "teacher","subject": 1}