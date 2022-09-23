import json

from django.urls import reverse
from django.urls import reverse

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from drf_user.models import User

from .models import Product, Payment
from .api.serializers import ProductSerializer, PaymentSerializer


class RegistrationTestCase(APITestCase):

    def test_registration(self):
        data = {"username": "testcase", "email": "test@localhost.app",
                "password": "some_strong_psw", "name": "John Shankar"}
        response = self.client.post("/api/user/register/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], "testcase")
        self.assertEqual(response.data["email"], "test@localhost.app")
        self.assertEqual(response.data["name"], "John Shankar")


class ProfileTestCase(APITestCase):
    profile_url = '/api/user/account/'

    def setUp(self):
        # username, email, name, password
        self.user = User.objects.create_user(username="testcase", email="test@localhost.app",
                                             password="some-very-strong-psw", name="John Doe")
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.api_authentication()

    def api_authentication(self):
        # Include an appropriate `Authorization:` header on all requests.
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

    def test_profile_authenticated(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_detail_retrieve(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "testcase")
        self.assertEqual(response.data["name"], "John Doe")

    def test_profile_update(self):
        response = self.client.patch(self.profile_url,
                                     {"username": "Marky", "name": "Mark Zuckerburg"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content),
                         {"id": 1, "username": "Marky", "name": "Mark Zuckerburg", "email": "test@localhost.app",
                          "mobile": None, "is_superuser": False, "is_staff": False})

