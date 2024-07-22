from datetime import timedelta

from rest_framework.exceptions import ValidationError


class RelatedOrRewardValidator:
    """Валидация по несовместимости 'связанной привычки' и 'вознаграждения'."""

    def __init__(self, field_1, field_2):
        self.field_1 = field_1
        self.field_2 = field_2

    def __call__(self, habit):
        if habit.get("connection_habit") and habit.get("reward"):
            raise ValidationError(
                "Нельзя одновременно выбирать связанную привычку и вознаграждение"
            )


class LeadTimeValidator:
    """Валидация по времени исполнения 'действия'(привычки)."""

    duration_time = timedelta(seconds=120)

    def __init__(self, field_1):
        self.field_1 = field_1

    def __call__(self, habit):
        if habit.get("duration") and habit.get("duration") > 120:
            raise ValidationError("Действие выполняется не более 2-х минут")


class CombinationValidator:
    """Валидация попадания в 'связанные привычки' только 'приятных привычек'."""

    def __init__(self, field_1, field_2):
        self.field_1 = field_1
        self.field_2 = field_2

    def __call__(self, habit):
        if habit.get("connection_habit"):
            if not habit.get("habit_is_pleasant"):
                raise ValidationError("Связанные привычки могут быть только приятными")


class NiceHabitValidator:
    """Валидация по отсутствию у 'приятной привычки' 'связанной привычки' или 'вознаграждения'."""

    def __init__(self, field_1, field_2, field_3):
        self.field_1 = field_1
        self.field_2 = field_2
        self.field_3 = field_3

    def __call__(self, habit):
        if habit.get("habit_is_pleasant"):
            if habit.get("connection_habit") or habit.get("reward"):
                raise ValidationError(
                    "У приятной привычки не может быть связанной привычки или вознаграждения"
                )


class PerformanceFrequencyValidator:
    """Валидация по частоте исполнения 'действия'(привычки)."""

    def __init__(self, field_1):
        self.field_1 = field_1

    def __call__(self, habit):
        number_list = [1, 2, 3, 4, 5, 6, 7]
        num = habit.get("number_of_executions")
        try:
            num in number_list
        except ValidationError:
            print("Привычку нельзя выполнять реже 1 и чаще 7 раз в неделю")