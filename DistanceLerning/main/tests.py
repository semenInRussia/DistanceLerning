from django.contrib.auth import authenticate
from django.test import TestCase, Client
from DistanceLerning.settings import VERSION
from auth_app.models import Subject

# Create your tests here.
from main.models import School


class SchoolTestCase(TestCase):
    username: str = "tester"
    email: str = "tester@email.com"
    password: str = "12234234faijrifejrafajeirg32JJIJEI"

    username_teacher: str = "tester_teacher"
    email_teacher: str = "tester_teacher@email.com"
    password_teacher: str = "12234234faijrifejrafajeirg32JJIJEI"

    new_username: str = "tester_new_directer"
    new_email: str = "tester_new_directer@email.com"
    new_password: str = "12234234faijrifejrafajeirg32JJIJEI"

    def setUp(self) -> None:
        self.client = Client()
        Subject.objects.create(name="History")

    def test_school_api_permissions_is_directer(self) -> None:
        resp = self.client.get(f'/api/{VERSION}/school/')

        # Not permissions
        self.assertEqual(
            resp.status_code, 403,
            "Status is available\n" +
            "Status would 403"
        )

        # Create User Teacher
        self.client.post(f"/api/{VERSION}/auth/", data={
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "role": "directer",
            "subject": "1",
        })

        # Login User Teacher
        self.client.post(f'/api/{VERSION}/auth/login/', data={
            "username": self.username,
            "password": self.password,
        })

        resp = self.client.get(f'/api/{VERSION}/school/')

        # Has permissions

        self.assertEqual(
            resp.status_code, 200,
            "Status is available\n" +
            "Status would 200"
        )

        # Create User
        self.client.post(f"/api/{VERSION}/auth/", data={
            "username": self.username_teacher,
            "email": self.email_teacher,
            "password": self.password_teacher,
            "role": "teacher",
            "subject": "1",
        })

        # Login User
        self.client.post(f'/api/{VERSION}/auth/login/', data={
            "username": self.username_teacher,
            "password": self.password_teacher,
        })

        resp = self.client.get(f'/api/{VERSION}/school/')

        # Not permissions

        self.assertEqual(
            resp.status_code, 403,
            "Status is available\n" +
            "Status would 403"
        )

    def test_school_api_permissions_id_owner_school(self) -> None:
        # Create User
        self.client.post(f"/api/{VERSION}/auth/", data={
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "role": "directer",
            "subject": "1",
        })

        # login user
        self.client.post(f"/api/{VERSION}/auth/login/", data={
            "username": self.username,
            "password": self.password,
        })

        user = authenticate(username=self.username,
                            password=self.password)

        school = School.objects.create(owner=user,
                                       number=500)

        # Delete school
        resp = self.client.delete(school.get_absolute_url())

        self.assertEqual(resp.status_code, 204,
                         "Status is not available. Status should is 204."
                         )
        self.client.post(f"/api/{VERSION}/auth/logout/")

        # Create new school
        school = School.objects.create(owner=user,
                                       number=500)
        # create new user
        self.client.post(f"/api/{VERSION}/auth/", data={
            "username": self.new_username,
            "email": self.new_email,
            "password": self.new_password,
            "role": "directer",
            "subject": "1",
        })

        # login new user
        self.client.post(f"/api/{VERSION}/auth/login/", data={
            "username": self.new_username,
            "password": self.new_password,
        })

        # get by school detail

        resp = self.client.delete(school.get_absolute_url())

        self.assertEqual(resp.status_code, 403,
                         "This status is available. Status should is 403"
                         )