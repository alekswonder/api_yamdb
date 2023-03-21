from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.models import User

USERNAME_ERROR = 'Имя должно содержать от 6 до 15 символов'
CONFIRM = 'Код подтверждения'
CONFIRM_NOTEFICATION = 'Ваш код подтверждения'


class AuthSerializer(serializers.Serializer):
    """Валидация юзернейма и кода подтверждения """
    username = serializers.CharField()
    email = serializers.EmailField()

    def validate_username(self, username):
        if len(username) < 6:
            raise ValidationError(USERNAME_ERROR)
        return username

    def get_confirm_code(self, **kwargs):
        user = User.objects.create(
            **self.validated_data, last_login=timezone.now()
        )
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            CONFIRM,
            f"{CONFIRM_NOTEFICATION}: {confirmation_code}",
            settings.ADMIN_EMAIL,
            [self.validated_data['email']],
        )


class UserSerializer(serializers.ModelSerializer):
    """Проверка данных юзера"""
    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('bio', 'email', 'first_name',
                  'last_name', 'role', 'username')


class AdminUserSerializer(serializers.ModelSerializer):
    """Проверка данных админа"""
    class Meta:
        model = User
        fields = ('bio', 'email', 'first_name',
                  'last_name', 'role', 'username')
