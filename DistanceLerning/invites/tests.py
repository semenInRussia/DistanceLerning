import json

from django.contrib.auth import get_user_model, authenticate
from django.test import TestCase, Client

from auth_app.models import Subject

from DistanceLerning.settings import VERSION

from main.models import School

User = get_user_model()

BASE_URL = f'/api/{VERSION}/'


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


class AnswerTestCase(TestCase):
    auth_url: str = BASE_URL + 'auth/'
    invite_send_url: str = BASE_URL + 'invite/send/'
    answer_send_url: str = BASE_URL + 'invite/answer/'

    username: str = 'tester'
    password: str = 'fkrigjtrgijriJFURJFURHF885548'
    email: str = 'tester@awai.com'

    new_username: str = 'testernew'
    new_password: str = 'fkrigjtrgijriJFURJFURHF885548'
    new_email: str = 'testerev@awai.com'

    def setUp(self) -> None:
        Subject.objects.create(name="History")

        self.client.post(self.auth_url, data={
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'role': 'directer',
            'subject': 1,
        })

        self.directer = authenticate(username=self.username,
                                     password=self.password)

        self.assertNotEqual(
            self.directer, None,
            'User is not authenticated'
        )

        self.client.post(self.auth_url, data={
            'username': self.new_username,
            'email': self.new_email,
            'password': self.new_password,
            'role': 'teacher',
            'subject': 1,
        })

        # save teacher
        self.teacher = authenticate(username=self.new_username,
                                    password=self.new_password)

        self.assertNotEqual(
            self.teacher, None,
            'User is not authenticated'
        )

        # login directer
        self.client.force_login(self.directer)

        # send invite from directer to teacher
        resp = self.client.post(self.invite_send_url, data={
            'username': self.new_username
        })

        print(resp.content.decode())
        data = json.loads(resp.content.decode())

        self.invite_id = data['pk']

        # logout
        self.client.logout()

    def test_send_answer(self):
        answer_text = 'I am working in other company!'

        # login teacher
        self.client.force_login(self.teacher)

        # send answer to directer
        resp_send_answer = self.client.post(self.answer_send_url, data={
            'invite': self.invite_id,
            'text': answer_text,
            'renouncement': False,
        })

        self.assertEqual(
            resp_send_answer.status_code, 201,
            'Status is not available. Status should is 201. Your status is {status}'.format(
                status=resp_send_answer.status_code)
        )

        self.client.logout()

        self.client.force_login(self.directer)

        # get answers
        resp_answer = self.client.get(self.answer_send_url)

        self.assertEqual(
            resp_answer.status_code, 200,
            'Status is not available. Status should is 200. Your status is {status}'.format(
                status=resp_answer.status_code)
        )

        data_string = resp_answer.content.decode()

        try:
            json_data = json.loads(data_string)
        except json.decoder.JSONDecodeError:
            self.assertTrue(False,
                            'String is not json')

        text = json_data[0]['text']

        self.assertEqual(
            text, answer_text,
            'Text is not available.'
        )
