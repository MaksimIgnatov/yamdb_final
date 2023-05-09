from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import CharField, TextChoices

username_validator = UnicodeUsernameValidator()


def validate_not_me_name(value):
    if value.lower() == 'me':
        raise ValidationError('Имя пользователя не может быть "me"')


class UserRole(TextChoices):
    USER = 'user', 'Пользователь'
    MODERATOR = 'moderator', 'Модератор'
    ADMIN = 'admin', 'Администратор'


class User(AbstractUser):
    """Кастомная модель Пользователя."""

    ROLE_CHOICES = UserRole
    bio = models.TextField(
        'Биография', blank=True, help_text='Расскажите о себе'
    )
    confirmation_code = models.CharField(
        'Код подтверждения', blank=True, max_length=150
    )
    email = models.EmailField(
        'Адрес электронной почты',
        max_length=254,
        blank=False,
        unique=True,
        help_text='Введите адрес электронной почты',
    )
    role = models.CharField(
        'Роль пользователя',
        choices=ROLE_CHOICES.choices,
        max_length=10,
        default=ROLE_CHOICES.USER,
        help_text='Выберите роль пользователя',
    )
    username = models.CharField(
        'Username',
        max_length=150,
        unique=True,
        help_text='Введите имя пользователя',
        validators=[username_validator, validate_not_me_name],
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self) -> CharField:
        return self.username

    def save(self, *args, **kwargs):
        if self.role == UserRole.MODERATOR:
            self.is_staff = True
            self.is_superuser = False
        if self.role == UserRole.ADMIN:
            self.is_staff = True
            self.is_superuser = True
        super().save(*args, **kwargs)

    @property
    def is_moderator(self):
        return self.role == UserRole.MODERATOR

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN or self.is_superuser
