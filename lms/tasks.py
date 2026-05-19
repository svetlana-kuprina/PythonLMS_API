from datetime import timedelta
from smtplib import SMTPException

from celery import shared_task
from django.core.mail import send_mail

from config import settings
from django.utils import timezone

from lms.models import Subscribe
from users.models import CustomUser


@shared_task
def send_email_update(data):
    mailing = Subscribe.objects.filter(course=data["course"]).all()

    result = []

    for mail_send in mailing:
        try:
            server_response = send_mail(
                subject=f"Обновление курса {mail_send.course.name}",
                message=f"Пользователь {mail_send.user.first_name} {mail_send.user.last_name} сообщаем, "
                        f"что курс {mail_send.course.name} обновился",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[
                    mail_send.user.email,
                ],
            )

            if server_response == 1:
                result.append(f"Письмо принято SMTP-сервером на адрес {mail_send.user.email}")
            else:
                result.append("Неизвестная ошибка отправки")

        except SMTPException as e:
            result.append(f"Ошибка SMTP: {str(e)}")

        except Exception as e:
            result.append(f"Внутренняя ошибка сервера: {str(e)}")

    return result


@shared_task
def deactivate_users():
    threshold = timezone.now() - timedelta(days=30)

    CustomUser.objects.filter(is_active=True, last_login__isnull=False, last_login__lt=threshold).update(
        is_active=False
    )
