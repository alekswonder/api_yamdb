from django.contrib.auth.models import AbstractUser
from django.db import models

from api_yamdb.settings import EMAIL_MAX_LENGTH, ROLE_MAX_LENGTH


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    roles_ru = ('Пользователь', 'Модератор', 'Администратор')
    CHOICES = (tuple(zip((USER, MODERATOR, ADMIN), roles_ru)))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.is_superuser:
            self.role = self.ADMIN

    email = models.EmailField(
        verbose_name='Email',
        unique=True,
        max_length=EMAIL_MAX_LENGTH
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=ROLE_MAX_LENGTH,
        choices=CHOICES,
        default=USER,
        db_index=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = (
            models.UniqueConstraint(
                fields=('username', 'email'),
                name='unique_users_fields'
            ),
        )
        ordering = ('role',)

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_user(self):
        return self.role == self.USER
