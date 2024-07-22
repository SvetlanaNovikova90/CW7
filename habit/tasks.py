import datetime

from habit.models import Habit
from habit.services import message_create, send_tg
from celery import shared_task


@shared_task
def send_message_tg():

    current_time = datetime.datetime.now().strftime("%X")

    habits = Habit.objects.all()

    for habit in habits:
        if habit.time == current_time:

            chat_id = habit.creator.chat_id
            if chat_id:
                count = habit.number_of_executions
                if count != 0:
                    text_message = message_create(habit.pk)
                    send_tg(chat_id=chat_id, message=text_message)
                    count -= 1
                    habit.save()
