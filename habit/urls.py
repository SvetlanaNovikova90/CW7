from django.urls import path

from habit.apps import HabitConfig
from habit.views import (
    HabitListApiView,
    HabitIsPublishedListApiView,
    HabitCreateApiView,
    HabitUpdateApiView,
    HabitDestroyApiView,
)

app_name = HabitConfig.name

urlpatterns = [
    path("habit/", HabitListApiView.as_view(), name="habit_list"),
    path(
        "habit_is_published/",
        HabitIsPublishedListApiView.as_view(),
        name="habit_is_published_list",
    ),
    path("habit/create/", HabitCreateApiView.as_view(), name="habit_create"),
    path("habit/update/<int:pk>/", HabitUpdateApiView.as_view(), name="habit_update"),
    path("habit/delete/<int:pk>/", HabitDestroyApiView.as_view(), name="habit_delete"),
]