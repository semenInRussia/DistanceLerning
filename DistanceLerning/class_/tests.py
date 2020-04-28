from django.test import TestCase

# Create your tests here.
from django.contrib.auth import authenticate, get_user_model
from django.test import TestCase, Client
from DistanceLerning.settings import VERSION

from .models import ClassModel
from auth_app.models import Subject
from main.models import School

User = get_user_model()


class ClassModelTestCase(TestCase):
    username: str = "tester"
    email: str = "tester@email.com"
    password: str = "12234234faijrifejrafajeirg32JJIJEI"

    new_username: str = "tester_new_directer"
    new_email: str = "tester_new_directer@email.com"
    new_password: str = "12234234faijrifejrafsgtrFEWFWdsfDfeDEWfwFEWfajeirg32JJIJEI"

    def setUp(self) -> None:
        Subject.objects.create(name="History")

        test_user = User.objects.create_user(email="directer@user.com",
                                             username="directer_username",
                                             password=self.password)

        self.school = School.objects.create(owner=test_user, number=400)

    def test_class_api_permissions_owner_class(self) -> None:
        # Create User
        self.client.post(f"/api/{VERSION}/auth/", data={
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "role": "directer",
            "subject": "1",
        })

        # login user
        self.client.login(username=self.username,
                          password=self.password)

        # Get user
        user = authenticate(username=self.username,
                            password=self.password)

        # Create class
        class_ = ClassModel.objects.create(char_class="a",
                                           number_class=1,
                                           owner=user,
                                           school=self.school)

        # Has permissions
        resp = self.client.delete(class_.get_absolute_url())

        self.assertEqual(
            resp.status_code, 204,
            "Status code is available. Status should is 204"
        )

        # Create class again
        class_ = ClassModel.objects.create(char_class="b",
                                           number_class=2,
                                           owner=user,
                                           school=self.school)

        # Logout user
        self.client.logout()

        # create new user
        self.client.post(f"/api/{VERSION}/auth/", data={
            "username": self.new_username,
            "email": self.new_email,
            "password": self.new_password,
            "role": "teacher",
            "subject": "1",
        })

        # login new user
        self.client.login(username=self.new_username,
                          password=self.new_password)

        # delete school detail
        resp = self.client.delete(class_.get_absolute_url())

        # Not permission
        self.assertEqual(resp.status_code, 403,
                         "This status is available. Status should is 403"
                         )