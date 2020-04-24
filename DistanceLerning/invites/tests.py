import json

from django.contrib.auth import get_user_model, authenticate
from django.test import TestCase, Client

from auth_app.models import Subject

from DistanceLerning.settings import VERSION

from main.models import School

User = get_user_model()


class InviteTestCase(TestCase):
    username: str = "tester"
    email: str = "tester@email.com"
    password: str = "pfriejf213jfuraiejfUFHfjraijr3jrfj"

    username_teacher: str = "tester_teacher"
    email_teacher: str = "tester_teacher@email.com"
    password_teacher: str = "pfriejf213jfuraiejfUFHfjraijr3jrfj"

    username_student: str = "tester_student"
    email_student: str = "tester_student@email.com"
    password_student: str = "pfriejf213jfuraiejfUFHfjraijr3jrfj"

    def setUp(self) -> None:
        self.client = Client()
        Subject.objects.create(name="History")

        self.client.post(f'/api/{VERSION}/auth/', data={
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "role": "directer",
            "subject": "1",
        })

        self.directer = authenticate(username=self.username,
                                     password=self.password)

        self.client.post(f'/api/{VERSION}/auth/', data={
            "username": self.username_student,
            "email": self.email_student,
            "password": self.password_student,
            "role": "student",
        })

        self.student = authenticate(username=self.username_student,
                                    password=self.password_student)

        self.client.post(f'/api/{VERSION}/auth/', data={
            "username": self.username_teacher,
            "email": self.email_teacher,
            "password": self.password_teacher,
            "role": "teacher",
            "subject": "1",
        })

        self.teacher = authenticate(username=self.username_teacher,
                                    password=self.password_teacher)

    def test_invite_send_to_teacher(self):
        # login directer
        self.client.force_login(self.directer)

        self.school = School.objects.create(owner=self.directer,
                                            number=500)

        resp = self.client.post(f'/api/{VERSION}/invite/send/', data={"username": self.username_teacher})

        self.assertEqual(
            resp.status_code, 201,
            "Status is available. Status should is 201"
        )

        self.client.logout()

        self.client.force_login(self.teacher)

        # get list
        resp = self.client.get(f'/api/{VERSION}/invite/list/')

        # Init json data
        json_data = []
        try:
            json_data = json.loads(resp.content.decode())
        except json.decoder.JSONDecodeError:
            pass

        try:
            username_ = json_data[0]["by_username"]
            self.assertEqual(
                username_, self.username,
                "User isn't send invite"
            )
        except IndexError:
            self.assertTrue(False,
                            "User isn't got invite"
                            )

        try:
            school_number = json_data[0]['school_number']

            self.assertEqual(
                school_number, self.school.number,
                "User isn't send invite"
            )
        except IndexError:
            self.assertTrue(False,
                            "User isn't got number school"
                            )
