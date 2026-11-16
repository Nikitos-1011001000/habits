from celery import shared_task
from django.utils import timezone

from .models import Habit
from .services import send_telegram_message


@shared_task
def send_habit_reminders():
    now = timezone.localtime()

    habits = Habit.objects.filter(
        user__telegram_chat_id__isnull=False,
    )

    for habit in habits:
        if habit.time.hour == now.hour and habit.time.minute == now.minute:
            message = (
                f"Напоминание: {habit.action} "
                f"в {habit.time.strftime('%H:%M')} "
                f"в {habit.place}."
            )
            send_telegram_message(habit.user.telegram_chat_id, message)
