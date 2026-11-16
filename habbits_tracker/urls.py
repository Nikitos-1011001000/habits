from django.urls import path

from .views import (
    HabitListCreateAPIView,
    HabitRetrieveUpdateDestroyAPIView,
    PublicHabitListAPIView,
)

urlpatterns = [
    path("habits/", HabitListCreateAPIView.as_view(), name="habit-list"),
    path("habits/<int:pk>/", HabitRetrieveUpdateDestroyAPIView.as_view(), name="habit-detail"),
    path("habits/public/", PublicHabitListAPIView.as_view(), name="public-habits"),
]
