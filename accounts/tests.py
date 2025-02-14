from django.test import TestCase
from django.contrib.auth import get_user_model
from ninja.errors import ValidationError, HttpError
from ninja.testing import TestClient
from accounts.models import AccountUser
from .utils import generate_username
from .api import router

UserModel = get_user_model()


class UserAPITest(TestCase):
    def setUp(self):
        self.client = TestClient(router)
        self.user = UserModel.objects.create_user(
            email="testuser@example.com",
            password="securepassword",
            username=generate_username(),
        )

    def test_login_success(self):
        response = self.client.post(
            "/api/accounts/login",
            {"email": "testuser@example.com", "password": "securepassword"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json())

    def test_login_failure(self):
        response = self.client.post(
            "/api/accounts/login",
            {"email": "testuser@example.com", "password": "wrongpassword"},
        )
        self.assertEqual(response.status_code, 401)

    def test_change_password(self):
        response = self.client.post(
            "/api/accounts/change-password",
            {"email": "testuser@example.com", "password": "newpassword"},
        )
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newpassword"))

    def test_retrieve_user(self):
        response = self.client.get(f"/api/accounts/{self.user.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["email"], "testuser@example.com")

    def test_update_user(self):
        response = self.client.patch(
            f"/api/accounts/{self.user.id}", {"username": "newusername"}
        )
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "newusername")

    def test_register_user(self):
        response = self.client.post(
            "/api/accounts/",
            {"email": "newuser@example.com", "password": "strongpassword"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(UserModel.objects.filter(email="newuser@example.com").exists())

    def test_list_users(self):
        response = self.client.get("/api/accounts")
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.json()["items"]), 1)
