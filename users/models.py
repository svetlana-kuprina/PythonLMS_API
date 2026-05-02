from django.contrib.auth.models import AbstractUser
from django.db import models

from lms.models import Course, Lesson


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="email")

    avatar = models.ImageField(
        upload_to="users/avatar/", null=True, blank=True, verbose_name="Аватар", help_text="Загрузите свой аватар"
    )
    telephone = models.CharField(
        max_length=20, verbose_name="Номер телефона", null=True, blank=True, help_text="Введите номер телефона"
    )
    country = models.CharField(max_length=50, verbose_name="Страна", null=True, blank=True, help_text="Введите страну")
    token = models.CharField(max_length=100, unique=True, verbose_name='Token', null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["email"]

    def __str__(self):
        return self.email


class Payments(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь',
                             help_text="Выберите пользователя")
    payment_date = models.DateField(verbose_name="Дата оплаты", null=True, blank=True,
                                    help_text="Дата оплаты курса или урока")
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Оплата курса', null=True,
                                    blank=True, related_name="paid_course")
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Оплата урока', null=True,
                                    blank=True, related_name="paid_lesson")
    payment_amount = models.DecimalField(max_digits=10,
                                         decimal_places=2,
                                         verbose_name="Сумма оплаты",
                                         null=True,
                                         blank=True,
                                         help_text="Сумма оплаты курса или урока"
                                         )
    STATUS_CHOICES = [
        ("cash", "Наличные"),
        ("translation", "Перевод на счет"),
    ]
    payment_method = models.CharField(max_length=100, choices=STATUS_CHOICES, default='cash',
                                      verbose_name="Способ оплаты")

    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Оплаты"
        ordering = ["payment_date"]

    def __str__(self):
        return f'{self.paid_course if self.paid_course else self.paid_lesson} - оплата {self.payment_method}'
