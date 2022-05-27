import hashlib
import random
from datetime import timedelta

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password, identify_hasher
from django.db.models import (EmailField, CharField, BooleanField, DateTimeField)
from django.utils.timezone import now

from post_inn.settings import TIME_DELTA_HOURS


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, name=None, full_name=None,
                    is_active=True, is_staff=None, is_admin=None):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('Пользователь должен иметь email адрес')
        if not password:
            raise ValueError('Пользователь должен ввести пароль')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.staff = is_staff
        user.admin = is_admin
        user.is_active = is_active
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, name=None):
        user = self.create_user(email, name=name, password=password,
                                is_staff=True, is_admin=True)
        return user

    def create_staffuser(self, email, password=None, name=None):
        user = self.create_user(email, name=name, password=password,
                                is_staff=True, is_admin=False)
        return user


class User(AbstractBaseUser):
    email = EmailField(unique=True, verbose_name='Email', max_length=255)
    name = CharField(verbose_name='Имя', max_length=255, blank=True, null=True)
    last_name = CharField(verbose_name='Фамилия', max_length=255, blank=True, null=True)
    staff = BooleanField(verbose_name='Сотрудник', default=False)
    is_active = BooleanField(verbose_name='Активный', default=True)
    admin = BooleanField(verbose_name='Администратор', default=False)
    timestamp = DateTimeField(verbose_name='Создан', auto_now_add=True)

    activation_key = CharField(max_length=128, blank=True)  # ключ подтверждения
    activation_key_expires = DateTimeField(default=(now() + timedelta(hours=TIME_DELTA_HOURS)))  # Срок действия ключа

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователя',
        verbose_name_plural = 'Пользователи',
        # list_display = ['email', 'name', 'staff', 'is_active', 'admin', 'timestamp']
        # ordering = ['-admin', 'staff', '-is_active']
        # ordering = ['timestamp']

    def is_activation_key_expired(self):
        if now() <= self.activation_key_expires:
            return False
        else:
            return True

    @staticmethod
    def create_key_expiration_date():
        return now() + timedelta(hours=TIME_DELTA_HOURS)

    @staticmethod
    def create_activation_key(email):
        salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
        return hashlib.sha1((email + salt).encode('utf8')).hexdigest()

    def __str__(self):
        return self.email

    def get_name(self):
        if self.name:
            return self.name
        return self.email

    def get_last_name(self):
        if self.last_name:
            return self.last_name
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        if self.admin:
            return True
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    def save(self, *args, **kwargs):
        try:
            # Узнаем алгоритм хеширования пароля
            _alg_hash = identify_hasher(self.password)
        except ValueError:
            # Если пароль не хешировался, получим исключение, проводим хеширование
            self.password = make_password(self.password)

        # if not self.id and not self.staff and not self.admin:
        #     self.password = make_password(self.password)
        super().save(*args, **kwargs)
