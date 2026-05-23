from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from users.models import Payments, CustomUser
from users.serializers import PaymentsSerializer, UserSerializer
from users.services import convert_rub_to_dollars, create_stripe_product, create_stripe_price, create_stripe_sessions


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

class PaymentsCreateAPIView(CreateAPIView):
    """Регистрация пользователя"""
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()


    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        if payment.paid_lesson is None:
            product_name = str(payment.paid_course)  # Преобразуем в строку
            print(f"Создаем продукт для курса: {product_name}")
        else:
            product_name = str(payment.paid_lesson)
            print(f"Создаем продукт для урока: {product_name}")

            # Создаем продукт в Stripe
        product = create_stripe_product(product_name)
        print(f"Продукт создан: {product.id}")

        # Конвертируем рубли в доллары
        amount_in_dollars = convert_rub_to_dollars(payment.payment_amount)
        print(f"Сумма в долларах: {amount_in_dollars}")

        # Создаем цену - используем product.id
        price = create_stripe_price(amount_in_dollars, product.id)
        print(f"Цена создана: {price.id}")

        # Создаем сессию
        session_id, payment_link = create_stripe_sessions(price)
        print(f"Сессия: {session_id}, Ссылка: {payment_link}")

        # Сохраняем данные
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()
