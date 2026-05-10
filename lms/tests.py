from click import group
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from django.contrib.auth.models import Group
from lms.models import Course, Lesson
from users.models import CustomUser


class LessonTests(APITestCase):
    """Тест CRUD уроков"""

    def setUp(self):
        self.user = CustomUser.objects.create_user(username='test', email="test@test.ru", password='123')
        self.course = Course.objects.create(name='test', description='test')
        self.lesson = Lesson.objects.create(name='test', description='test', course=self.course, owner=self.user)

        self.client.force_authenticate(user=self.user)

    def test_lesson_detail(self):
        url = reverse('lms:lesson-detail', args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.lesson.name)

    def test_lesson_list(self):
        url = reverse('lms:lesson-list')
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("count"), 1)
        self.assertEqual(data.get("results")[0].get("name"), self.lesson.name)

    def test_lesson_create(self):
        url = reverse('lms:lesson-create')
        data = {
            "name": "Урок № 9 PHP111",
            "description": "Курс по PHP,CSS,HTML9",
            "video_url": "https://youtube.com/eks/pavodki",
            "course": self.course.pk
        }
        response = self.client.post(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_lesson_update(self):
        url = reverse('lms:lesson-update', args=(self.lesson.pk,))
        data = {"name": "Урок № 9 PHP111111", }
        response = self.client.patch(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "Урок № 9 PHP111111")

    def test_lesson_delete(self):
        url = reverse('lms:lesson-delete', args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class LessonTestsManager(APITestCase):
    """Тест CRUD уроков c правами менеджер"""

    def setUp(self):
        group_name_moderator = "moders"
        self.group, created = Group.objects.get_or_create(name=group_name_moderator)
        self.user = CustomUser.objects.create_user(username='test', email="test@test.ru", password='123')
        self.user.groups.add(self.group)
        self.course = Course.objects.create(name='test', description='test')
        self.course = Course.objects.create(name='test', description='test')
        self.lesson = Lesson.objects.create(name='test', description='test', course=self.course, owner=self.user)

        self.client.force_authenticate(user=self.user)

    def test_lesson_detail(self):
        url = reverse('lms:lesson-detail', args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.lesson.name)

    def test_lesson_list(self):
        url = reverse('lms:lesson-list')
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("count"), 1)
        self.assertEqual(data.get("results")[0].get("name"), self.lesson.name)

    def test_lesson_create(self):
        url = reverse('lms:lesson-create')
        data = {
            "name": "Урок № 9 PHP111",
            "description": "Курс по PHP,CSS,HTML9",
            "video_url": "https://youtube.com/eks/pavodki",
            "course": self.course.pk
        }
        response = self.client.post(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_update(self):
        url = reverse('lms:lesson-update', args=(self.lesson.pk,))
        data = {"name": "Урок № 9 PHP111111", }
        response = self.client.patch(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "Урок № 9 PHP111111")

    def test_lesson_delete(self):
        url = reverse('lms:lesson-delete', args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)