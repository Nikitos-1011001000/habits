from rest_framework import serializers

from .models import Habit
from .validators import (
    validate_duration,
    validate_periodicity,
    validate_pleasant_habit,
    validate_related_habit,
    validate_reward_or_related,
)


class HabitSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    related_habit = serializers.PrimaryKeyRelatedField(
        queryset=Habit.objects.all(),
        allow_null=True,
        required=False,
    )

    class Meta:
        model = Habit
        fields = (
            "id",
            "user",
            "place",
            "time",
            "action",
            "is_pleasant",
            "related_habit",
            "periodicity",
            "reward",
            "duration",
            "is_public",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("user", "created_at", "updated_at")

    def validate(self, attrs):
        duration = attrs.get("duration")
        periodicity = attrs.get("periodicity")

        if duration is not None:
            validate_duration(duration)

        if periodicity is not None:
            validate_periodicity(periodicity)

        validate_reward_or_related(attrs)
        validate_pleasant_habit(attrs)
        validate_related_habit(attrs)

        return attrs
