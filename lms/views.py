from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from lms.models import Course, Lesson, Subscribe
from lms.paginators import CustomPagination
from lms.serializers import CourseSerializer, LessonSerializer, SubscriptionsSerializer
from users.permissions import IsModer, IsOwner


class LMSViewSet(ModelViewSet):
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
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPagination

class LessonDetail(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner,)

class LessonCreate(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (~IsModer, IsAuthenticated)


    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

class LessonUpdate(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner,)

class LessonDelete(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsOwner | ~IsModer)


class SubscriptionsAPIView(APIView):
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