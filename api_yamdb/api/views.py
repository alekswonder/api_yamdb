from django.contrib.auth.tokens import default_token_generator
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User

CONFIRM_ERROR = 'Неверный код подтвержения'

class AuthViewSet(viewsets.GenericViewSet):
    """Регистрация и получение кода подтверждения"""
    permission_classes = (permissions.AllowAny,)
    serializer_class = AuthSerializer

    @action(detail=False, methods=['POST'])
    def signup(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(Q(
            username=serializer.data.get('username')
        ) | Q(
            email=serializer.data.get('email')
        ))
        if user:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer.get_confirm_code()
        return Response(serializer.data, status.HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def token(self, request):
        if (not request.data.get('username')
                or not request.data.get('confirmation_code')):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(User, username=request.data.get('username'))
        confirmation_code = request.data.get('confirmation_code')
        if not default_token_generator.check_token(user, confirmation_code):
            return Response(CONFIRM_ERROR,
                            status=status.HTTP_400_BAD_REQUEST)
        user.is_active = True
        user.save()
        refresh = RefreshToken.for_user(user)
        tokens = dict(access_token=str(refresh.access_tokens),
                      refresh_token=str(refresh))
        return Response(tokens, status=status.HTTP_200_OK)
