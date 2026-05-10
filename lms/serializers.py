from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from lms.models import Course, Lesson

class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(ModelSerializer):
    count_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_count_lessons(self, obj):
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = ("id", "name", "preview", "description", "count_lessons", "lessons","owner")

    def create(self, validated_data):
        lessons = validated_data.pop("lessons")

        course_item = Course.objects.create(**validated_data)
        for lesson in lessons:
            Lesson.objects.create(**lesson, lesson = course_item)

        return course_item


