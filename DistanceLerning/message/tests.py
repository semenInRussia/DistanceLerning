import json

from django.contrib.auth import authenticate
from django.test import TestCase
from django.conf import settings

# Create your tests here.

BASE_URL = f'/api/{settings.VERSION}/'


class MessageTestCase(TestCase):
    auth_url: str = BASE_URL + 'auth/'
    message_url: str = BASE_URL + 'message/'

    msg_text: str = 'You are wanted'
    msg_subject: str = 'Super subject'

    username: str = 'tester'
    email: str = 'tester@gmail.com'
    password: str = 'grsmij9fjriejgijfriIFJIR'

    new_username: str = 'new_tester'
    new_email: str = 'new_tester@gmail.com'
    new_password: str = 'grsmij9fjriejgijfriIFJIR'

    def setUp(self) -> None:
        self.client.post(self.auth_url, data={
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'role': 'student'
        })

        # Get user
        self.student1 = authenticate(username=self.username,
                                    password=self.password)

        self.client.post(self.auth_url, data={
            'username': self.new_username,
            'email': self.new_email,
            'password': self.new_password,
            'role': 'student'
        })

        # Get user
        self.student2 = authenticate(username=self.new_username,
                                     password=self.new_password)

        self.assertNotEqual(
            self.student2, None,
            'User is not authenticated'
        )

    def test_send_message(self):
        # send
        send_response = self.client.post(self.message_url, {
            'to': self.student1.pk,
            'text': self.msg_text,
        })

        # assert created
        self.assertEqual(
            send_response.status_code, 201,
            'Status is not available. Status should is 201. Your status {status}'.format(
                status=send_response.status_code
            )
        )

        # Login recipient
        self.client.force_login(self.student1)

        # get messages
        message_response = self.client.get(self.message_url)

        # assert OK
        self.assertEqual(
            message_response.status_code, 200,
            'Status is not available. Status should is 200. Your status is {status}'.format(
                status=message_response.status_code
            )
        )

        # get data
        data_string = message_response.content.decode()
        data_json = json.loads(data_string)

        text = data_json[0]['text']
        subject = data_json[0]['subject']

        self.assertEqual(
            text, self.msg_text,
            'Text is not gated.'
        )

        self.assertEqual(
            subject, self.msg_subject,
            'Subject is not gated.'
        )
