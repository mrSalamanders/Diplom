from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from phonenumber_field.modelfields import PhoneNumberField
# from phonenumber_field.formfields import PhoneNumberField


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, first_name=None, last_name=None, is_active=True, is_staff=False, is_superuser=False):
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have a password')

        user_obj = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )
        user_obj.active = is_active
        user_obj.staff = is_staff
        user_obj.superuser = is_superuser
        user_obj.set_password(password)    # change user password
        user_obj.save(using=self._db)
        return user_obj

    def create_staff_user(self, email, password=None):
        user_obj = self.create_user(
            email,
            password=password,
            is_staff=True
        )
        return user_obj

    def create_superuser(self, email, password=None):
        user_obj = self.create_user(
            email,
            password=password,
            is_staff=True,
            is_superuser=True
        )
        return user_obj


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        null=False,
        blank=False,
        unique=True,
        max_length=80,
        verbose_name='Email'
    )
    phone = PhoneNumberField(
        verbose_name='Телефон',
        null=False,
        blank=False
    )
    first_name = models.CharField(
        null=True,
        blank=True,
        max_length=80,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        null=True,
        blank=True,
        max_length=80,
        verbose_name='Фамилия'
    )
    active = models.BooleanField(
        default=True,
        verbose_name='Активен?'
    )
    staff = models.BooleanField(
        default=False,
        verbose_name='Работник?'
    )
    superuser = models.BooleanField(
        default=False,
        verbose_name='Админ?'
    )

    USERNAME_FIELD = 'email'    # username
    # USERNAME_FIELD and password are required by default
    REQUIRED_FIELDS = []    # python manage.py createsuperuser

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_short_name(self):
        if self.first_name:
            return self.first_name
        return self.email

    def get_full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.email

    @property
    def is_active(self):
        return self.active

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_superuser(self):
        return self.superuser

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class GuestEmail(models.Model):
    full_name = models.CharField(
        max_length=240,
        verbose_name='Полное имя'
    )
    phone = PhoneNumberField(
        verbose_name='Телефон',
        null=False,
        blank=False
    )
    email = models.EmailField()
    reason = models.TextField(verbose_name='Причина обращения')
    seen = models.BooleanField(verbose_name='Обработан', default=False)
    updated_at = models.DateField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Обращение"
        verbose_name_plural = "Обращения"
