import json

from django.contrib.auth import authenticate
from django.test import TestCase, Client
from django.conf import settings
from auth_app.models import Subject

# Create your tests here.
from main.models import School

VERSION = settings.VERSION

BASE_URL = f'/api/{VERSION}'


class SchoolTestCase(TestCase):
    bind_school_url: str = BASE_URL + '/bind-school/'
    auth_url: str = BASE_URL + '/auth/'
    send_invite_url: str = BASE_URL + '/invite/send/'
    list_invite_url: str = BASE_URL + '/invite/list/'
    send_answer_url: str = BASE_URL + '/invite/answer/'

    username: str = "tester"
    email: str = "tester@email.com"
    password: str = "12234234faijrifejrafajeirg32JJIJEI"

    username_directer2: str = "username_directer2"
    email_directer2: str = "email_directer2@email.com"
    password_directer2: str = "12234234faijrifejrafajeirg32JJIJEI"

    username_teacher: str = "tester_teacher"
    email_teacher: str = "tester_teacher@email.com"
    password_teacher: str = "12234234faijrifejrafajeirg32JJIJEI"

    new_username: str = "tester_new_directer"
    new_email: str = "tester_new_directer@email.com"
    new_password: str = "12234234faijrifejrafajeirg32JJIJEI"

    def setUp(self) -> None:
        Subject.objects.create(name="History")
        # Create User Teacher
        self.client.post(f"/api/{VERSION}/auth/", data={
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "role": "teacher",
            "subject": "1",
        })

        self.teacher1 = authenticate(username=self.username,
                                     password=self.password)

        # Create User
        self.client.post(f"/api/{VERSION}/auth/", data={
            "username": self.username_teacher,
            "email": self.email_teacher,
            "password": self.password_teacher,
            "role": "teacher",
            "subject": "1",
        })

        self.teacher2 = authenticate(username=self.username_teacher,
                                     password=self.password_teacher)

        self.client.post(f"/api/{VERSION}/auth/", data={
            "username": self.new_username,
            "email": self.new_email,
            "password": self.new_password,
            "role": "directer",
            "subject": "1",
        })

        self.directer = authenticate(username=self.new_username,
                                     password=self.new_password)

        self.client.post(self.auth_url, data={
            "username": self.username_directer2,
            "email": self.email_directer2,
            "password": self.password_directer2,
            "role": "directer",
            "subject": '1',
        })

        self.directer2 = authenticate(username=self.username_directer2,
                                      password=self.password_directer2)

        self.assertNotEqual(
            self.directer2, None,
            'Directer is not authenticated'
        )

    def test_school_api_permissions_is_directer(self) -> None:
        resp = self.client.get(f'/api/{VERSION}/school/')

        # Not permissions
        self.assertEqual(
            resp.status_code, 403,
            "Status is available\n" +
            "Status would 403"
        )

        self.client.force_login(self.directer)

        resp = self.client.get(f'/api/{VERSION}/school/')

        # Has permissions

        self.assertEqual(
            resp.status_code, 200,
            "Status is available\n" +
            "Status would 200"
        )

        # Login User
        self.client.force_login(self.teacher1)

        resp = self.client.get(f'/api/{VERSION}/school/')

        # Not permissions

        self.assertEqual(
            resp.status_code, 403,
            "Status is available\n" +
            "Status would 403"
        )

    def test_school_api_permissions_is_owner_school(self) -> None:
        # Create User
        self.client.force_login(self.directer)

        user = authenticate(username=self.username,
                            password=self.password)

        school = School.objects.create(owner=self.directer,
                                       number=500)

        # Delete school
        resp = self.client.delete(school.get_absolute_url())

        self.assertEqual(resp.status_code, 204,
                         "Status is not available. Status should is 204."
                         )
        self.client.post(f"/api/{VERSION}/auth/logout/")

        # Create new school
        school = School.objects.create(owner=self.directer,
                                       number=520)

        # login directer 2
        self.client.force_login(self.directer2)

        # get by school detail
        resp = self.client.delete(school.get_absolute_url())

        self.assertEqual(resp.status_code, 403,
                         "This status is available. Status should is 403"
                         )

    def test_school_user_bind(self) -> None:
        School.objects.create(owner=self.directer,
                              number=1200)

        # login directer
        self.client.force_login(self.directer)

        self.client.post(self.send_invite_url, data={
            "username": self.teacher1.username,
        })

        # logout
        self.client.logout()

        # login teacher
        self.client.force_login(self.teacher1)

        # watch invites
        get_invites_resp = self.client.get(self.list_invite_url)

        invites_string = get_invites_resp.content.decode()

        json_data = json.loads(invites_string)
        print(json_data)
        first_invite_id = json_data[0]['pk']
        school_number = json_data[0]['school_number']

        # Send answer
        self.client.post(self.send_answer_url, data={
            'invite': first_invite_id,
            'renouncement': True,
            'text': 'OK',
        })

        bind_teacher_resp = self.client.post(path=self.bind_school_url, data={
            'school_number': school_number,
        })

        self.assertEqual(
            bind_teacher_resp.status_code, 201,
            f'Teacher\'s and school\'s bind status is not available. '
            f'Status should is 201. '
            f'Your status is {bind_teacher_resp.status_code}.'
        )
