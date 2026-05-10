from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from users.models import Payments, CustomUser
from users.serializers import PaymentsSerializer, UserSerializer


class PaymentsAPIView(ModelViewSet):
    """Фильтрация и сортировка"""
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ("paid_lesson", "paid_course", "payment_method")
    ordering_fields = ("payment_date",)


class UserCreateAPIView(CreateAPIView):
    """Регистрация пользователя"""
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()
