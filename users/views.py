from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet

from users.models import Payments
from users.serializers import PaymentsSerializer


class PaymentsAPIView(ModelViewSet):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ("paid_lesson", "paid_course", "payment_method")
    ordering_fields = ("payment_date",)
