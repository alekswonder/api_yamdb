from django.contrib import admin

from .models import Genre, Category, Title


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Настройка панели администратора для модели Title(Произведения)"""
    list_display = ('name', 'year', 'description',
                    'genre', 'category')
    list_filter = ('genre', 'category', 'year')
    search_fields = ('name', 'description')
    ordering = ('genre', 'category', 'year')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Настройка панели администратора для модели Genre(Жанр)"""
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Category)
class Category(admin.ModelAdmin):
    """Настройка панели администратора для модели Category(Категории)"""
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
