from django.urls import path
from rest_framework.routers import SimpleRouter
from lms.views import LMSViewSet, LessonList, LessonDetail, LessonCreate, LessonUpdate, LessonDelete
from lms.apps import LmsConfig


app_name = LmsConfig.name

router = SimpleRouter()
router.register("", LMSViewSet)


urlpatterns = [
    path('lesson/', LessonList.as_view(), name='lesson-list'),
    path('lesson/create/', LessonCreate.as_view(), name='lesson-create'),
    path('lesson/<int:pk>', LessonDetail.as_view(), name='lesson-detail'),
    path('lesson/<int:pk>/update', LessonUpdate.as_view(), name='lesson-update'),
    path('lesson/<int:pk>/delete', LessonDelete.as_view(), name='lesson-delete'),
]
urlpatterns += router.urls