from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Модель пользователя"""

    email = models.EmailField(unique=True, verbose_name="email")

    avatar = models.ImageField(
        upload_to="users/avatar/", null=True, blank=True, verbose_name="Аватар", help_text="Загрузите свой аватар"
    )
    telephone = models.CharField(
        max_length=20, verbose_name="Номер телефона", null=True, blank=True, help_text="Введите номер телефона"
    )
    country = models.CharField(max_length=50, verbose_name="Страна", null=True, blank=True, help_text="Введите страну")
    token = models.CharField(max_length=100, unique=True, verbose_name="Token", null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["email"]

    def __str__(self):
        return self.email


class Payments(models.Model):
    """Модель оплаты курсов и уроков"""

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, verbose_name="Пользователь", help_text="Выберите пользователя"
    )
    payment_date = models.DateField(
        verbose_name="Дата оплаты", null=True, blank=True, help_text="Дата оплаты курса или урока"
    )
    paid_course = models.ForeignKey(
        "lms.Course",
        on_delete=models.CASCADE,
        verbose_name="Оплата курса",
        null=True,
        blank=True,
        related_name="paid_course",
    )
    paid_lesson = models.ForeignKey(
        "lms.Lesson",
        on_delete=models.CASCADE,
        verbose_name="Оплата урока",
        null=True,
        blank=True,
        related_name="paid_lesson",
    )
    payment_amount = models.PositiveIntegerField(
        verbose_name="Сумма оплаты", default=0, help_text="Сумма оплаты курса или урока"
    )
    session_id = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Id сессии", help_text="Введите Id сессии"
    )
    link = models.URLField(
        max_length=500, null=True, blank=True, verbose_name="Ссылка на оплату", help_text="Введите ссылку на оплату"
    )

    STATUS_CHOICES = [
        ("cash", "Наличные"),
        ("translation", "Перевод на счет"),
    ]
    payment_method = models.CharField(
        max_length=100, choices=STATUS_CHOICES, default="translation", verbose_name="Способ оплаты"
    )

    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Оплаты"
        ordering = ["payment_date"]

    def __str__(self):
        return (
            f"{self.paid_course if self.paid_course else self.paid_lesson} - оплата {self.payment_method},"
            f" {self.payment_date}, {self.payment_amount}, {self.link}"
        )
