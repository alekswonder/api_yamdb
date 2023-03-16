from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class AuthSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
