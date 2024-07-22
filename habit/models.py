from django.db import models
from datetime import timedelta
from config.settings import AUTH_USER_MODEL


class Habit(models.Model):

    creator = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Создатель",
    )
    place = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Место выполнения"
    )
    time = models.TimeField(blank=True, null=True, verbose_name="Время выполнения")
    action = models.CharField(max_length=100, verbose_name="Действие")
    habit_is_pleasant = models.BooleanField(
        default=True, verbose_name="Признак приятной привычки"
    )
    connection_habit = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Связанная привычка",
    )
    number_of_executions = models.IntegerField(
        default=1, verbose_name="Количество выполнений в неделю"
    )
    duration = models.DurationField(
        default=timedelta(seconds=120), verbose_name="Продолжительность выполнения"
    )
    is_published = models.BooleanField(default=True, verbose_name="Признак публичности")
    reward = models.CharField(
        max_length=100, verbose_name="Вознаграждение", blank=True, null=True
    )

    def __str__(self):
        return f"Действие: {self.action}(создатель {self.creator})"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
