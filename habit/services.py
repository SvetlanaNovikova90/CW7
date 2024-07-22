import requests
from config.settings import TELEGRAM_TOKEN, TELEGRAM_URL
from habit.models import Habit


def message_create(habit_id):
    """Создание сообщения."""

    habit = Habit.objects.get(id=habit_id)

    user = habit.creator
    name = name_of_user(user.email)

    time = habit.time
    if habit.place is None:
        place = ""
    else:
        place = habit.place

    action = habit.action

    if habit.connection_habit_id:
        message = (
            f"Привет {name}! Уже ({time})! Давай быстрей, пора ({action}),"
            f" в ({place}),"
            f" за это ты можешь: {Habit.objects.get(id=habit.connection_habit_id).action}!"
        )
    elif habit.reward:
        message = (
            f"Привет {name}! Уже ({time})! Давай быстрей, пора({action}),"
            f" в ({place}), за это ты можешь: {habit.reward}!"
        )
    else:
        message = (
            f"Привет {name}! Уже ({time})! Давай быстрей, пора({action})," f" в ({place})."
        )

    return message


def send_tg(chat_id, message):
    params = {
        "text": message,
        "chat_id": chat_id,
    }
    requests.post(f"{TELEGRAM_URL}{TELEGRAM_TOKEN}/sendMessage", params=params)


def name_of_user(email):
    """Формируем имя из почты."""
    name = ""
    for letter in email:
        if letter != "@":
            name += letter
        else:
            break
    return name
