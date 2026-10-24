import pyotp
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from accounts.models import UserProfile


class UserProfileModelTestCase(TestCase):
    def test_profile_created_with_totp_key(self):
        user = User.objects.create_user(username="tester", password="pass12345")

        profile = UserProfile.objects.get(user=user)
        assert profile.totp_key
        assert user.userprofile == profile


class UsersApiTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="tester", password="pass12345")

    def test_my_anonymous(self):
        r = self.client.get("/api/users/my/")
        data = r.json()

        assert r.status_code == 200
        assert data["is_authenticated"] is False
        assert data["id"] is None

    def test_my_authenticated(self):
        self.client.force_authenticate(user=self.user)

        data = self.client.get("/api/users/my/").json()

        assert data["is_authenticated"] is True
        assert data["id"] == self.user.id
        assert data["username"] == "tester"

    def test_login_success(self):
        r = self.client.post("/api/users/login/", {"username": "tester", "password": "pass12345"})
        assert r.status_code == 200

        data = self.client.get("/api/users/my/").json()
        assert data["is_authenticated"] is True

    def test_login_wrong_password(self):
        r = self.client.post("/api/users/login/", {"username": "tester", "password": "wrong"})
        assert r.status_code == 401

    def test_logout(self):
        self.client.post("/api/users/login/", {"username": "tester", "password": "pass12345"})
        r = self.client.post("/api/users/logout/")
        assert r.status_code == 200

        data = self.client.get("/api/users/my/").json()
        assert data["is_authenticated"] is False

    def test_second_login_valid_code(self):
        self.client.force_authenticate(user=self.user)
        code = pyotp.TOTP(self.user.userprofile.totp_key).now()

        r = self.client.post("/api/users/second-login/", {"key": code})
        assert r.status_code == 200

    def test_second_login_invalid_code(self):
        self.client.force_authenticate(user=self.user)

        r = self.client.post("/api/users/second-login/", {"key": "not-a-code"})
        assert r.status_code == 400