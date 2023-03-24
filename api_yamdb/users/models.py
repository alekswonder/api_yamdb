from django.contrib.auth.models import AbstractUser
from django.db import models
from api.validators import validate_username


class User(AbstractUser):
    """Кастомная модель юзера"""
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = (
        ('user', 'user'), ('moderator', 'moderator'), ('admin', 'admin')
    )
    username = models.CharField(max_length=150,
                                unique=True,
                                validators=[validate_username])
    first_name = models.CharField(verbose_name='Имя',
                                  max_length=150,
                                  blank=True)
    last_name = models.CharField(verbose_name='Фамилия',
                                 max_length=150,
                                 blank=True)
    email = models.EmailField(verbose_name='Почта',
                              unique=True,
                              max_length=254)
    bio = models.TextField(verbose_name='Биография',
                           blank=True,)
    role = models.CharField(max_length=30,
                            choices=ROLE_CHOICES,
                            default='user')

    def save(self, *args, **kwargs):
        if self.role == 'admin':
            self.is_superuser = True
        elif self.role == 'moderator':
            self.is_staff = True
        super().save(*args, **kwargs)
