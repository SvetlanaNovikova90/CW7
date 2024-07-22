from datetime import timedelta
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from habit.models import Habit
from users.models import User


class HabitTestCase(APITestCase):
    """Тесты привычки."""

    def setUp(self):
        self.user = User.objects.create(email="admin@example.com")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.habit = Habit.objects.create(
            creator=self.user,
            place="Дома",
            time="08:00:00",
            action="Выпить стакан воды",
            habit_is_pleasant=False,
            connection_habit=None,
            number_of_executions=5,
            duration=timedelta(seconds=120),
            is_published=True,
            reward="Послушать песню",
        )

    def test_habit_list(self):
        """Тест вывода списка привычек."""

        url = reverse("habit:habit_list")
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Habit.objects.all().count(), 1)

    def test_habit_is_published_list(self):
        """Тест вывода списка публичных привычек."""

        url = reverse("habit:habit_is_published_list")
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Habit.objects.all().count(), 1)

    def test_habit_create(self):
        """Тест создания привычки."""

        url = reverse("habit:habit_create")
        data = {
            "action": "Лечь спать вовремя",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 2)

    def test_habit_update(self):
        """Тестируем изменение привычки."""

        url = reverse("habit:habit_update", args=(self.habit.pk,))
        data = {
            "reward": "Съесть яблоко",
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("reward"), "Съесть яблоко")

    def test_habit_delete(self):
        """Тест удаления привычки."""

        url = reverse("habit:habit_delete", args=(self.habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.all().count(), 0)
