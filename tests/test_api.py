from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class HabitAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="user1",
            email="user1@example.com",
            password="StrongPassword123!",
        )
        self.client.force_authenticate(user=self.user)

    def test_create_habit(self):
        url = reverse("habit-list")
        data = {
            "place": "Дом",
            "time": "19:00",
            "action": "Сделать зарядку",
            "duration": 60,
            "periodicity": 1,
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["action"], "Сделать зарядку")

    def test_user_sees_only_own_habits(self):
        other_user = User.objects.create_user(
            username="user2",
            email="user2@example.com",
            password="StrongPassword123!",
        )

        from habbits_tracker.models import Habit

        Habit.objects.create(
            user=other_user,
            place="Парк",
            time="08:00",
            action="Прогулка",
            duration=30,
        )

        url = reverse("habit-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)

    def test_duration_validator(self):
        url = reverse("habit-list")
        data = {
            "place": "Дом",
            "time": "19:00",
            "action": "Медитация",
            "duration": 150,
            "periodicity": 1,
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AuthAPITests(APITestCase):
    def setUp(self):
        self.register_url = "/api/register/"
        self.login_url = "/api/login/"
        self.refresh_url = "/api/token/refresh/"
        self.me_url = "/api/me/"

        self.user_data = {
            "username": "nikita",
            "email": "nikita@example.com",
            "password": "StrongPassword123!",
            "password2": "StrongPassword123!",
            "telegram_chat_id": "123456789",
        }

    def test_register_user(self):
        response = self.client.post(
            self.register_url,
            self.user_data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertTrue(
            User.objects.filter(username="nikita").exists(),
        )

    def test_register_with_mismatched_passwords(self):
        data = self.user_data.copy()
        data["password2"] = "AnotherPassword123!"

        response = self.client.post(
            self.register_url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_login_returns_tokens(self):
        self.client.post(
            self.register_url,
            self.user_data,
            format="json",
        )

        response = self.client.post(
            self.login_url,
            {
                "username": "nikita",
                "password": "StrongPassword123!",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_refresh_token(self):
        self.client.post(
            self.register_url,
            self.user_data,
            format="json",
        )

        login_response = self.client.post(
            self.login_url,
            {
                "username": "nikita",
                "password": "StrongPassword123!",
            },
            format="json",
        )

        refresh_token = login_response.data["refresh"]

        response = self.client.post(
            self.refresh_url,
            {"refresh": refresh_token},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertIn("access", response.data)

    def test_me_requires_authentication(self):
        response = self.client.get(self.me_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_me_returns_current_user(self):
        self.client.post(
            self.register_url,
            self.user_data,
            format="json",
        )

        login_response = self.client.post(
            self.login_url,
            {
                "username": "nikita",
                "password": "StrongPassword123!",
            },
            format="json",
        )

        access_token = login_response.data["access"]
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )

        response = self.client.get(self.me_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data["username"],
            "nikita",
        )

    def test_me_update_telegram_chat_id(self):
        self.client.post(
            self.register_url,
            self.user_data,
            format="json",
        )

        login_response = self.client.post(
            self.login_url,
            {
                "username": "nikita",
                "password": "StrongPassword123!",
            },
            format="json",
        )

        access_token = login_response.data["access"]
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {access_token}",
        )

        response = self.client.patch(
            self.me_url,
            {"telegram_chat_id": "987654321"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data["telegram_chat_id"],
            "987654321",
        )
