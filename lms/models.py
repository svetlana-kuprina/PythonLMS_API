from django.db import models

from users.models import CustomUser


class Course(models.Model):
    """Модель: Курс"""

    name = models.CharField(max_length=150, null=True, blank=True, verbose_name="Название")
    preview = models.ImageField(
        upload_to="lms/preview/", null=True, blank=True, verbose_name="Превью", help_text="Загрузите превью"
    )
    description = models.TextField(null=True, blank=True, verbose_name="Описание")
    owner = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Владелец",
                              help_text="Укажите владельца")

    def __str__(self):
        return f"Наименование курса: {self.name}"

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ["name"]


class Lesson(models.Model):
    """Модель: Урок"""

    name = models.CharField(max_length=150, null=True, blank=True, verbose_name="Название урока")
    preview = models.ImageField(
        upload_to="lms/preview/", null=True, blank=True, verbose_name="Превью", help_text="Загрузите превью"
    )

    description = models.TextField(null=True, blank=True, verbose_name="Описание")
    video_url = models.URLField(null=True, blank=True, verbose_name="Ссылка на видео", help_text="Ссылка на видео")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons',
                               verbose_name="Курс")
    owner = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Владелец",
                              help_text="Укажите владельца")

    def __str__(self):
        return f"Наименование урока: {self.name}"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Урок"
        ordering = ["name"]


class Subscribe(models.Model):
    """Модель подписки на курс"""
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="subs_course",
        verbose_name="Курс подписки",
        help_text="Подписка на курс",
    )

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="subs_user",
        verbose_name="Пользователь",
        help_text="Пользователь",
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        ordering = ["course", "user"]

    def __str__(self):
        return f"{self.course} {self.user}"
