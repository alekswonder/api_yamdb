from django.contrib import admin

from .models import Genre, Category, Title, Comment, Review


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Настройка панели администратора для модели Title(Произведения)"""
    list_display = ('name', 'year', 'get_genres', 'description', 'category')
    list_filter = ('genre', 'category', 'year')
    search_fields = ('name', 'description')
    ordering = ('genre', 'category', 'year')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Настройка панели администратора для модели Genre(Жанр)"""
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Настройка панели администратора для модели Category(Категории)"""
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('review', 'text', 'author', 'pub_date',)
    search_fields = ('review',)
    list_filter = ('review',)
    empty_value_display = '-пусто-'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'author', 'score',)
    search_fields = ('pub_date',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'
