from django.db.models import Avg

from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError

from api.validators import validate_username
from titles.models import Category, Genre, Title
from reviews.models import Review, Comment
from users.models import User


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(required=True,
                                     max_length=150,
                                     validators=(validate_username,))
    email = serializers.EmailField(required=True,
                                   max_length=254)

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        user_first = User.objects.filter(username=username).first()
        user_second = User.objects.filter(email=email).first()
        if user_first != user_second:
            raise serializers.ValidationError(
                f'Пользователь с таким username:{username}'
                f' или email:{email} уже существует.'
            )
        return data


class CustomUserSerializer(serializers.ModelSerializer):
    """Сериализация объектов типа User."""
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                f'Создать пользователя с username:{value} невозможно'
            )
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                f'Создать пользователя с email:{value} невозможно'
            )
        return value


class GenreSerializer(serializers.ModelSerializer):
    """Сериализация объектов типа Genre"""
    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_fields = 'slug'
        extra_kwargs = {
            'url': {'lookup_fields': 'slug'}
        }


class CategorySerializer(serializers.ModelSerializer):
    """Сериализация объектов типа Category"""
    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_fields = 'slug'
        extra_kwargs = {
            'url': {'lookup_fields': 'slug'}
        }


class TitleListSerializer(serializers.ModelSerializer):
    """Сериализация для безопасных запросов модели Title"""
    rating = serializers.SerializerMethodField()
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        model = Title
        read_only_fields = fields

    def get_rating(self, obj):
        """Среднеарифметическое значение оценок,
        относящихся к одному произведению
        """
        rating = obj.reviews.aggregate(Avg('score')).get('score__avg')
        return round(rating, 1) if rating else None


class TitleCreateSerializer(serializers.ModelSerializer):
    """Сериализация для небезопасных запросов модели Title"""
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )

    class Meta:
        fields = ('name', 'year', 'description', 'genre', 'category')
        model = Title
        read_only_fields = ('category',)


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

    class Meta:
        model = Review
        fields = '__all__'

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
        fields = '__all__'
