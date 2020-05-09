import json

from django.contrib.auth import get_user_model, authenticate
from django.test import TestCase, Client
from DistanceLerning.settings import VERSION
from .models import Subject, Student, Diary, Teacher, Directer, ActivationCode

BASE_URL = "/api/{VERSION}/".format(VERSION=VERSION)

User = get_user_model()


# Create your tests here.
class AuthTestCase(TestCase):
    username_student: str = 'tester'
    password_student: str = "1234567f"
    email_student: str = "tester@email.com"

    username: str = 'tester_student'
    password: str = "1234567f"
    email: str = "tester_student@email.com"

    username_teacher: str = 'tester_teacher'
    password_teacher: str = "1234567f"
    email_teacher: str = "tester_teacher@email.com"

    username_directer: str = 'tester_directer'
    password_directer: str = "1234567f"
    email_directer: str = "tester_directer@email.com"

    def setUp(self) -> None:
        # Template create User

        # self.client.post(f'/api/{VERSION}/auth/', data={
        #     'username': self.username,
        #     'email': self.email,
        #     'password': self.password,
        #     'role': 'teacher',
        #     'subject': 1,
        # })

        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0')

        # create subjects
        Subject.objects.create(name="History")
        Subject.objects.create(name="Math")

    def test_auth_POST(self):
        resp = self.client.post(f'/api/{VERSION}/auth/', data={
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'role': 'student',
        })

        self.assertEqual(
            resp.status_code, 201,
            "Status is not available"
        )

        # Get user
        user = authenticate(username=self.username,
                            password=self.password)

        self.assertEqual(user.username, self.username,
                         "User is not created")

        self.assertNotEqual(user, None,
                            "User is not defined")

    def test_auth_POST_student(self):
        resp = self.client.post(f'/api/{VERSION}/auth/', data={
            'username': self.username_student,
            'email': self.email_student,
            'password': self.password_student,
            'role': 'student',
        })

        self.assertEqual(
            resp.status_code, 201,
            "Status is not available"
        )

        # Get user
        user = authenticate(username=self.username_student,
                            password=self.password_student)

        # User is defined?
        self.assertNotEqual(user, None,
                            "User is not defined")

        # User is created?
        self.assertEqual(
            User.objects.count(), 1,
            "User is not created..."
        )

        self.assertEqual(
            Student.objects.count(), 1,
            "Student is not created..."
        )

    def test_auth_POST_teacher(self):
        resp = self.client.post(f'/api/{VERSION}/auth/', data={
            'username': self.username_teacher,
            'email': self.email_teacher,
            'password': self.password_teacher,
            'role': 'teacher',
            'subject': 1,
        })

        self.assertEqual(
            resp.status_code, 201,
            "Status is not available"
        )

        # Get user
        user = authenticate(username=self.username_teacher,
                            password=self.password_teacher)

        # User is defined?
        self.assertNotEqual(user, None,
                            "User is not defined")

        # User is created?
        self.assertEqual(
            User.objects.count(), 1,
            "User is not created..."
        )

        # Teacher is created?
        self.assertEqual(
            Teacher.objects.count(), 1,
            'Teacher is not created'
        )

    def test_auth_POST_directer(self):
        resp = self.client.post(f'/api/{VERSION}/auth/', data={
            'username': self.username_directer,
            'email': self.email_directer,
            'password': self.password_directer,
            'role': 'directer',
            "subject": 1,
        })

        self.assertEqual(
            resp.status_code, 201,
            "Status is not available"
        )

        # Get user
        user = authenticate(username=self.username_directer,
                            password=self.password_directer)

        # User is defined?
        self.assertNotEqual(user, None,
                            "User (Directer) is not defined")

        # User is created?
        self.assertEqual(
            User.objects.count(), 1,
            "User  (Directer) is not created..."
        )

        # Teacher is created?
        self.assertEqual(
            Directer.objects.count(), 1,
            'Directer is not created'
        )

    def test_login(self):
        # False login
        resp = self.client.post(f'/api/{VERSION}/auth/login/', data={
            'username': self.username,
            'password': self.password,
        })
        self.assertEqual(
            resp.status_code, 403,
            'Status is not available\n'
            'Status is 403'
        )

        # Create User
        self.client.post(f'/api/{VERSION}/auth/', data={
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'role': 'student',
        })

        # Login
        resp = self.client.post(f'/api/{VERSION}/auth/login/', data={
            'username': self.username,
            'password': self.password,
        })

        self.assertEqual(
            resp.status_code, 200,
            'Status is not available'
            '\n Status is 200'
        )

    def test_logout(self) -> None:
        # False Logout
        resp = self.client.post(f'/api/{VERSION}/auth/logout/', data={
            'username': self.username,
            'password': self.password,
        })
        self.assertEqual(
            resp.status_code, 403,
            'Status is not available\n'
            'Status is 403'
        )

        # Create User
        self.client.post(f'/api/{VERSION}/auth/', data={
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'role': 'student',
        })

        # Login
        self.client.post(f'/api/{VERSION}/auth/login/', data={
            'username': self.username,
            'password': self.password,
        })

        # Logout
        resp = self.client.post(f'/api/{VERSION}/auth/logout/')

        self.assertEqual(
            resp.status_code, 200,
            'Status is not available\n'
            'Status is 200'
        )

class ActivationCodeTestCase(TestCase):
    auth_url = BASE_URL + 'auth/'
    activate_url = BASE_URL + 'auth/activate/'
    me_url = BASE_URL + 'auth/me/'

    password = 'password'
    username = 'username'

    def setUp(self) -> None:
        # create user
        self.client.post(self.auth_url, data={
            'username': self.username,
            'password': self.password,
            'email': 'email@email.com',
            'role': 'student',
        })

        self.test_user = authenticate(username=self.username,
                                      password=self.password)

    def test_activate(self) -> None:
        # login user
        self.client.force_login(self.test_user)
        # get activation code
        self.assertEqual(
            ActivationCode.objects.count(), 1,
            'ActivationCode is not created'
        )

        activation_code = ActivationCode.objects.get(user=self.test_user)
        code = activation_code.code

        activate_resp = self.client.post(self.activate_url, data={'code': code})

        self.assertEqual(
            activate_resp.status_code, 200,
            'Activate status code is not valid. '
            'Status should is 200 '
            'Your status is {}'.format(activate_resp.status_code)
        )

        profile_data = self.client.get(self.me_url)
        profile_data_string = profile_data.content.decode()
        profile_data_json = json.loads(profile_data_string)

        self.assertEqual(
            profile_data_json.get('is_active'), True,
            'User is not activated.'
        )

