import smtplib
import logging
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from post_inn import settings
from post_inn.utils import logger


def send_verify_mail(user):
    """
    Confirm registration by email
    :param user:
    :return: количество успешно доставленных сообщений (которое может быть 0 или 1)
    """

    try:
        verify_link = reverse('authapp:verify', args=[user.email, user.activation_key])
        title = f'Подтверждение учетной записи {user.email}'
        message = f'Для подтверждения учетной записи {user.email}, на сайте {settings.DOMAIN_NAME} - пройдите по ссылке: ' \
                  f'{settings.DOMAIN_NAME}{verify_link}'

        # fail_silently = False, в случае неудачной отправки, генерируется ошибка smtplib.SMTPException)
        result_send_message = send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
        logger.info(f'Пользователю {user.email} отправлена ссылка для подтверждения регистрации')
        return result_send_message

    except smtplib.SMTPException as err:
        logging.error(f'При отправке письма произошло исключение: {err}')
        return 0

    except Exception as err:
        logging.error(f'При отправке письма произошло исключение: {err.args[0]}', exc_info=True)
        return 0


def send_reset_password(user):
    """
    Send email to reset user password
    :param user:
    :return: количество успешно доставленных сообщений (которое может быть 0 или 1)
    """
    title = f'Запрошен сброс пароля на сайте {settings.DOMAIN_NAME}'
    uid = urlsafe_base64_encode(force_bytes(user.pk)),  # шифруем идентификатор
    token = default_token_generator.make_token(user),  # генерируем токен
    verify_link = str(reverse('authapp:password_reset_confirm', args=[uid[0], token[0]]))
    logger.debug(f'Для пользователя {user.email} сгенерирована ссылка для сброса пароля {verify_link}')
    message = f'Для сброса пароля на сайте {settings.DOMAIN_NAME} - пройдите по ссылке: /' \
              f' {settings.DOMAIN_NAME}{verify_link}. Если Вы не запрашивали смену пароля - проигнорируйте это письмо.'

    try:
        send_message = send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
        return send_message

    except smtplib.SMTPException as err:
        logging.error(f'При отправке письма произошло исключение: {err}')

    except Exception as err:
        logging.error(f'При отправке письма произошло исключение: {err.args[0]}', exc_info=True)
        return 0
