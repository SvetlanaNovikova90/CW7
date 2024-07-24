from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated

from habit.models import Habit
from habit.paginations import CustomPagination
from habit.permissions import IsOwner
from habit.serializers import HabitSerializer
from habit.tasks import send_message_tg


class HabitListApiView(ListAPIView):
    """ Вьюсет списка привычек"""
    serializer_class = HabitSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Habit.objects.all()
        elif user.is_authenticated:
            return Habit.objects.filter(creator=user)


class HabitIsPublishedListApiView(ListAPIView):
    """ Вьюсет списка публичных привычек"""
    serializer_class = HabitSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Habit.objects.filter(is_published=True)


class HabitCreateApiView(CreateAPIView):
    """ Вьюсет создания привычки"""
    serializer_class = HabitSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        send_message_tg()


class HabitUpdateApiView(UpdateAPIView):
    """ Вьюсет изменения привычки"""
    serializer_class = HabitSerializer
    permission_classes = (
        IsAuthenticated,
        IsOwner,
    )

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Habit.objects.filter(creator=user)


class HabitDestroyApiView(DestroyAPIView):
    """ Вьюсет удаления привычки"""
    permission_classes = (IsOwner,)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Habit.objects.filter(creator=user)
