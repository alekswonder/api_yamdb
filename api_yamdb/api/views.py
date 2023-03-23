from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, mixins, permissions, status, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .filters import TitleFilterSet
from .serializers import (GenreSerializer, CategorySerializer,
                          CommentSerializer, ReviewSerializer, AuthSerializer,
                          AdminUserSerializer, UserSerializer,
                          TitleListSerializer, TitleCreateSerializer)
from titles.models import Title, Genre, Category, Review
from .pagination import ComplexObjectPagination
from .permissions import (CustomAdminPermission, SafeMethodAdminPermission,)
from users.models import User

CONFIRM_ERROR = 'Неверный код подтверждения'


class ListCreateDestroyViewSet(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    pass


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
        tokens = dict(access_token=str(refresh.access_token),
                      refresh_token=str(refresh))
        return Response(tokens, status=status.HTTP_200_OK)


class TitleViewSet(viewsets.ModelViewSet):
    """Представление модели Title."""
    queryset = Title.objects.all()
    serializer_class = TitleListSerializer
    pagination_class = ComplexObjectPagination
    permission_classes = (SafeMethodAdminPermission, )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilterSet

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleListSerializer
        return TitleCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        output = TitleListSerializer(instance=Title.objects.last())
        return Response(
            output.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        output = TitleListSerializer(instance=self.get_object())
        return Response(output.data)


class GenreViewSet(ListCreateDestroyViewSet):
    """Представление модели Genre."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_classes = PageNumberPagination
    permission_classes = (SafeMethodAdminPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(ListCreateDestroyViewSet):
    """Представление модели Category."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_classes = PageNumberPagination
    permission_classes = (SafeMethodAdminPermission,)
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    """Представление модели Review."""
    serializer_class = ReviewSerializer
    pagination_class = ComplexObjectPagination
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Представление модели Comment."""
    serializer_class = CommentSerializer
    pagination_class = ComplexObjectPagination
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)


class UserViewSet(viewsets.ModelViewSet):
    """Работа с юзерами"""
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = (CustomAdminPermission,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    filterset_fields = ('username',)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(detail=False, methods=['GET', 'PATCH'],
            permission_classes=(IsAuthenticated,))
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PATCH':
            if user.role == 'user':
                serializer = UserSerializer(user,
                                            data=request.data, partial=True)
            else:
                serializer = AdminUserSerializer(user, data=request.data,
                                                 partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
