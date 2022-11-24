import smtplib
import logging
import base64
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from post_inn import settings
from post_inn.utils import logger


def create_encoded_byte_str(txt: str) -> str:
    """Create encoded byte string"""
    try:
        txt_byte = txt.encode('utf-8')
        txt_b64 = base64.urlsafe_b64encode(txt_byte).decode("utf-8")
        return txt_b64

    except Exception as err:
        err_message = f'Error: при кодировании данных произошла ошибка. Мы уже работаем над ней'
        logging.critical(f'При кодировании данных произошло исключение: {err}')
        return err_message


def create_decoded_byte_str(txt: str) -> str:
    """Create decoded byte string"""
    try:
        txt_byte = txt.encode('utf-8')
        txt_str = base64.urlsafe_b64decode(txt_byte).decode("utf-8")
        return txt_str

    except Exception as err:
        logging.critical(f'При декодировании данных произошло исключение: {err}')


def send_verify_mail(user):
    """
    Confirm registration by email
    :param user:
    :return: количество успешно доставленных сообщений (которое может быть 0 или 1)
    """
    try:
        email_b64 = create_encoded_byte_str(user.email)
        verify_link = reverse('authapp:verify', args=[email_b64, user.activation_key])
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
        result_send_message = send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
        return result_send_message

    except smtplib.SMTPException as err:
        logging.error(f'При отправке письма произошло исключение: {err}')
        return 0

    except Exception as err:
        logging.error(f'При отправке письма произошло исключение: {err.args[0]}', exc_info=True)
        return 0
