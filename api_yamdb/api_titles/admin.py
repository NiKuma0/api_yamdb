from django.contrib import admin
from .models import Genres, Categories, Titles


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    empty_value_display = '-пусто-'


@admin.register(Genres)
class GenresAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    empty_value_display = '-пусто-'


@admin.register(Titles)
class TitlesAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'category')
    empty_value_display = '-пусто-'
