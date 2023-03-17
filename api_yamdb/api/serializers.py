from rest_framework import serializers

from titles.models import Category, Genre, Title, GenreTitle


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    genres = GenreSerializer(many=True)
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )

    class Meta:
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genres', 'category')
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
        """Происходит агрегирующий запрос по среднему арифметическому значению
        по полю 'score' таблицы Review, которые относятся к таблице Title,
        через обратное отношение
        Пример: obj - экземпляр класса Title
        Мы через обратное отношение review_set, либо related_name
        obj.review_set.aggregate(Avg('score'))
        получаем среднеарифметическое всех оценок
        """
        return 0


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category
