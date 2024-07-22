from rest_framework import serializers

from habit.models import Habit
from habit.validators import (
    RelatedOrRewardValidator,
    LeadTimeValidator,
    CombinationValidator,
    NiceHabitValidator,
    PerformanceFrequencyValidator,
)


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Habit."""

    class Meta:
        model = Habit
        fields = "__all__"

        validators = [
            RelatedOrRewardValidator("connection_habit", "reward"),
            LeadTimeValidator("duration"),
            CombinationValidator("connection_habit", "habit_is_pleasant"),
            NiceHabitValidator("habit_is_pleasant", "connection_habit", "reward"),
            PerformanceFrequencyValidator("number_of_executions"),
        ]
