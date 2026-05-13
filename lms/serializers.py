from rest_framework import serializers


from lms.models import Course, Lesson, Subscribe
from lms.validators import validate_lesson


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(validators=[validate_lesson])

    class Meta:
        model = Lesson
        fields = '__all__'



class CourseSerializer(serializers.ModelSerializer):
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


class SubscriptionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscribe
        fields = '__all__'