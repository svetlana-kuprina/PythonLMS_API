
from rest_framework.serializers import ModelSerializer
from users.models import Payments, CustomUser


class PaymentsSerializer(ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'

class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
