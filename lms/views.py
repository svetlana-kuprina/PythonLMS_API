from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from lms.models import Course, Lesson, Subscribe
from lms.paginators import CustomPagination
from lms.serializers import CourseSerializer, LessonSerializer, SubscriptionsSerializer
from lms.tasks import send_email_update
from users.permissions import IsModer, IsOwner, IsNotModerator


class LMSViewSet(ModelViewSet):
    """CRUD viewset for Course"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()


    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = (~IsModer,)
        elif self.action in ['update', 'retrieve']:
            self.permission_classes = (IsModer | IsOwner,)
        elif self.action in ['destroy',]:
            self.permission_classes = (~IsModer | IsOwner,)
        return super().get_permissions()


class LessonList(ListAPIView):
    """Вывод списка уроков"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPagination

class LessonDetail(RetrieveAPIView):
    """Вывод урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner,)

class LessonCreate(CreateAPIView):
    """Добавление урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (~IsModer, IsAuthenticated)


    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()
        send_email_update.delay(serializer.data)


class LessonUpdate(UpdateAPIView):
    """Редактирование урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner,)

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)
        send_email_update.delay(serializer.data)

class LessonDelete(DestroyAPIView):
    """Удаление урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsNotModerator | IsOwner)

    def perform_destroy(self, instance):
        data = LessonSerializer(instance).data
        instance.delete()
        send_email_update.delay(data)


class SubscriptionsAPIView(APIView):
    """Активация подписки на курс"""

    serializer_class = SubscriptionsSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = kwargs['pk']

        course = Course.objects.get(id=course_id)
        subscription = Subscribe.objects.filter(user=user, course=course)

        if subscription.exists():
            subscription.delete()
            message = "Подписка успешно удалена"
        else:
            Subscribe.objects.create(user=user, course=course)
            message = "Подписка успешно добавлена"

        return Response({"message": message})