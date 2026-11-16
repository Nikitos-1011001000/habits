from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habbits_tracker.models import Habit
from users.models import User


class HabitViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="user1",
            email="user1@example.com",
            password="StrongPassword123!",
        )
        self.other_user = User.objects.create_user(
            username="user2",
            email="user2@example.com",
            password="StrongPassword123!",
        )

        self.client.force_authenticate(user=self.user)

        self.list_url = reverse("habit-list")

        self.valid_data = {
            "place": "Дом",
            "time": "19:00",
            "action": "Сделать зарядку",
            "duration": 60,
            "periodicity": 1,
        }

    def test_create_habit(self):
        response = self.client.post(
            self.list_url,
            self.valid_data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertEqual(
            Habit.objects.count(),
            1,
        )

    def test_user_sees_only_own_habits(self):
        Habit.objects.create(
            user=self.other_user,
            place="Парк",
            time="08:00",
            action="Прогулка",
            duration=30,
        )

        response = self.client.get(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data["count"],
            0,
        )

    def test_retrieve_own_habit(self):
        habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="19:00",
            action="Сделать зарядку",
            duration=60,
        )

        url = reverse(
            "habit-detail",
            args=[habit.id],
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data["action"],
            "Сделать зарядку",
        )

    def test_update_own_habit(self):
        habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="19:00",
            action="Сделать зарядку",
            duration=60,
        )

        url = reverse(
            "habit-detail",
            args=[habit.id],
        )

        response = self.client.patch(
            url,
            {"action": "Сделать растяжку"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        habit.refresh_from_db()
        self.assertEqual(
            habit.action,
            "Сделать растяжку",
        )

    def test_delete_own_habit(self):
        habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="19:00",
            action="Сделать зарядку",
            duration=60,
        )

        url = reverse(
            "habit-detail",
            args=[habit.id],
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertFalse(
            Habit.objects.filter(id=habit.id).exists(),
        )

    def test_cannot_update_other_user_habit(self):
        habit = Habit.objects.create(
            user=self.other_user,
            place="Парк",
            time="08:00",
            action="Прогулка",
            duration=30,
        )

        url = reverse(
            "habit-detail",
            args=[habit.id],
        )

        response = self.client.patch(
            url,
            {"action": "Взлом"},
            format="json",
        )

        self.assertIn(
            response.status_code,
            [
                status.HTTP_403_FORBIDDEN,
                status.HTTP_404_NOT_FOUND,
            ],
        )

    def test_public_habits_list(self):
        Habit.objects.create(
            user=self.other_user,
            place="Парк",
            time="08:00",
            action="Прогулка",
            duration=30,
            is_public=True,
        )

        url = reverse("public-habits")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data["count"],
            1,
        )
