from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import (viewsets, mixins, permissions,
                            status, filters, serializers)
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api_yamdb import settings
from .filters import TitleFilterSet
from .serializers import (GenreSerializer, CategorySerializer,
                          CommentSerializer, ReviewSerializer,
                          TitleListSerializer, TitleCreateSerializer,
                          UserSerializer, SignUpSerializer)
from titles.models import Title, Genre, Category
from reviews.models import Review
from .pagination import ComplexObjectPagination
from .permissions import (AdminOnly, IsAdminOrReadOnly,
                          IsAdminOrAuthorOrModeratorOrReadOnly)
from users.models import User


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class ListCreateDestroyViewSet(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    pass


class GenreCategoryViewSet(ListCreateDestroyViewSet):
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class SignUpViewSet(viewsets.GenericViewSet):
    """Регистрация и получение кода подтверждения"""
    permission_classes = (permissions.AllowAny,)
    serializer_class = SignUpSerializer

    @action(detail=False, methods=['POST'])
    def signup(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data.get('username')
        email = serializer.data.get('email')
        try:
            user, is_created = User.objects.get_or_create(username=username,
                                                          email=email
                                                          )
        except IntegrityError:
            raise serializers.ValidationError(f'Что-то не так с'
                                              f' username: {username}'
                                              f' или email: {email}')
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Код подтверждения YaMDb',
            message=f'Ваш код подтверждения: {confirmation_code}',
            from_email=settings.ADMIN_EMAIL,
            recipient_list=(user.email,)
        )
        return Response(serializer.data, status.HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def token(self, request):
        if (not request.data.get('username')
                or not request.data.get('confirmation_code')):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(User, username=request.data.get('username'))
        confirmation_code = request.data.get('confirmation_code')
        if not default_token_generator.check_token(user, confirmation_code):
            return Response('Неверный код подтверждения',
                            status=status.HTTP_400_BAD_REQUEST)

        refresh = get_tokens_for_user(user)
        return Response({'token': refresh['access']},
                        status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """Работа с юзерами"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    filterset_fields = ('username',)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ('get', 'post', 'patch', 'delete')

    @action(detail=False, methods=['GET', 'PATCH'],
            permission_classes=(IsAuthenticated,))
    def me(self, request):
        user = get_object_or_404(User,
                                 username=request.user.username
                                 )
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(user,
                                         data=request.data,
                                         partial=True
                                         )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TitleViewSet(viewsets.ModelViewSet):
    """Представление модели Title."""
    queryset = Title.objects.all()
    serializer_class = TitleListSerializer
    pagination_class = ComplexObjectPagination
    permission_classes = (IsAdminOrReadOnly,)
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


class GenreViewSet(GenreCategoryViewSet):
    """Представление модели Genre."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(GenreCategoryViewSet):
    """Представление модели Category."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Представление модели Review."""
    serializer_class = ReviewSerializer
    pagination_class = ComplexObjectPagination
    permission_classes = (IsAdminOrAuthorOrModeratorOrReadOnly,)
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)

    def perform_update(self, serializer):
        super(ReviewViewSet, self).perform_update(serializer)


class CommentViewSet(viewsets.ModelViewSet):
    """Представление модели Comment."""
    serializer_class = CommentSerializer
    pagination_class = ComplexObjectPagination
    permission_classes = (IsAdminOrAuthorOrModeratorOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)
