from django.db.models import Avg
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils import timezone

from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError

from titles.models import Category, Genre, Title, GenreTitle, Review, Comment
from users.models import User

USERNAME_ERROR = 'Имя должно содержать от 6 до 15 символов'
CONFIRM = 'Код подтверждения'
CONFIRM_NOTIFICATION = 'Ваш код подтверждения'


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
            f"{CONFIRM_NOTIFICATION}: {confirmation_code}",
            settings.ADMIN_EMAIL,
            [self.validated_data['email']],
        )


class GenreSerializer(serializers.ModelSerializer):
    """Сериализация объектов типа Genre"""
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    """Сериализация объектов типа Title"""
    rating = serializers.SerializerMethodField()
    genre = GenreSerializer(many=True)
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )

    class Meta:
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        model = Title
        read_only_fields = ('category',)

    def create(self, validated_data):
        if 'genres' not in self.initial_data:
            title = Title.objects.create(**validated_data)
            return title

        genres = validated_data.pop('genres')
        title = Title.objects.create(**validated_data)
        for genre in genres:
            current_genre, status = Genre.objects.get_or_create(**genre)
            GenreTitle.objects.create(genre=current_genre, title=title)
        return title

    def get_rating(self, obj):
        """Среднеарифметическое значение оценок,
        относящихся к одному произведению
        """
        return obj.reviews.aggregate(Avg('score'))


class CategorySerializer(serializers.ModelSerializer):
    """Сериализация объектов типа Category"""
    class Meta:
        fields = ('name', 'slug')
        model = Category


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализация объектов типа Review."""
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )

    def validate(self, data):
        request = self.context['request']
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(
                title=title, author=request.user
            ).exists():
                raise ValidationError('Вы не можете добавить более'
                                      'одного отзыва на произведение')
        return data

    def validate_score(self, value):
        if value < 1 or value > 10:
            raise ValidationError(
                f'Недопустимое значение, {value} должен быть от 1 до 10.'
            )
        return value

    class Meta:
        model = Review
        exclude = ('title',)


class CommentSerializer(serializers.ModelSerializer):
    """Сериализация объектов типа Comment."""
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        exclude = ('review',)
