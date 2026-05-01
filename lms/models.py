from django.db import models


class Course(models.Model):
    """Модель: Курс"""

    name = models.CharField(max_length=150, null=True, blank=True, verbose_name="Название")
    preview = models.ImageField(
        upload_to="lms/preview/", null=True, blank=True, verbose_name="Превью", help_text="Загрузите превью"
    )
    description = models.TextField(null=True, blank=True, verbose_name="Описание")


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

    def __str__(self):
        return f"Наименование урока: {self.name}"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Урок"
        ordering = ["name"]

