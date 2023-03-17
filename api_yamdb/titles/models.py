from django.db import models


class Title(models.Model):
    """Модель произведений, к которым пишут отзывы"""
    name = models.CharField(
        max_length=255,
        verbose_name='Название'
    )
    year = models.PositiveIntegerField(
        verbose_name='Год создания',
        db_index=True
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        'Genre',
    )
    category = models.ForeignKey(
        'Category',
        null=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        ordering = ('id',)
        default_related_name = 'titles'
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def get_genres(self):
        """Получаем названия жанров для отображения их в админ панели"""
        return '\n'.join([g.name for g in self.genre.all()])

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанров произведений"""
    name = models.CharField(
        max_length=255,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'


class Category(models.Model):
    """Модель категорий произведений"""
    name = models.CharField(
        max_length=255,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name
