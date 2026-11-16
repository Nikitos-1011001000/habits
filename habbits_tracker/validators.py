from django.core.exceptions import ValidationError

MAX_DURATION = 120
MAX_PERIODICITY = 7


def validate_duration(value):
    if value > MAX_DURATION:
        raise ValidationError(
            f"Время выполнения не может превышать {MAX_DURATION} секунд."
        )


def validate_periodicity(value):
    if value < 1 or value > MAX_PERIODICITY:
        raise ValidationError(
            f"Привычку нельзя выполнять реже одного раза в {MAX_PERIODICITY} дней."
        )


def validate_reward_or_related(data):
    reward = data.get("reward")
    related_habit = data.get("related_habit")

    if reward and related_habit:
        raise ValidationError(
            "Нельзя одновременно указать вознаграждение и связанную привычку."
        )


def validate_pleasant_habit(data):
    is_pleasant = data.get("is_pleasant")
    reward = data.get("reward")
    related_habit = data.get("related_habit")

    if is_pleasant and (reward or related_habit):
        raise ValidationError(
            "У приятной привычки не может быть вознаграждения или связанной привычки."
        )


def validate_related_habit(data):
    related_habit = data.get("related_habit")

    if related_habit and not related_habit.is_pleasant:
        raise ValidationError(
            "Связанной может быть только приятная привычка."
        )
