from django.core.management.base import BaseCommand

from lms.models import Course, Lesson
from users.models import CustomUser, Payments


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        user = CustomUser.objects.get(id=1)
        course1 = Course.objects.get(id=1)
        lesson3 = Lesson.objects.get(id=2)

        courses = [
            {'user':user, 'payment_date':'2026-05-01', 'paid_course':course1, 'payment_amount': 1000 },
            {'user':user, 'payment_date':'2026-05-01', 'paid_lesson':lesson3, 'payment_amount': 2000 },
        ]

        for course_data in courses:
            course, created = Payments.objects.get_or_create(**course_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Создана оплата: {course}'))
            else:
                self.stdout.write(self.style.WARNING(f'Book already exists: {course}'))
