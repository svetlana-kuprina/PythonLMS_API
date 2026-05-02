from django.urls import path
from rest_framework.routers import SimpleRouter


from users.apps import UsersConfig
from users.views import PaymentsAPIView

app_name = UsersConfig.name

router = SimpleRouter()
router.register("", PaymentsAPIView)


urlpatterns = []
urlpatterns += router.urls