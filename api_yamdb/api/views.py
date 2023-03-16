from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions

from .serializers import AuthSerializer

User = get_user_model()


class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = AuthSerializer
