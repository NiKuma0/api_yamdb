from django.contrib import admin
from .models import Review, Comment


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'score', 'text', 'pub_date')
    empty_value_display = '-пусто-'
    search_fields = ('title', 'author', 'text')
    list_filter = ('title', 'pub_date')
    ordering = 'pub_date'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'author', 'review', 'pub_date')
    empty_value_display = '-пусто-'
    list_filter = ('pub_date',)
    search_fields = ('text', 'author')
