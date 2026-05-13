from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.apps import UsersConfig
from users.views import PaymentsAPIView, UserCreateAPIView, PaymentsCreateAPIView

app_name = UsersConfig.name

router = SimpleRouter()
router.register("", PaymentsAPIView)


urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="register" ),
    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
    path('payment/', PaymentsCreateAPIView.as_view(), name='payment'),

]
urlpatterns += router.urls