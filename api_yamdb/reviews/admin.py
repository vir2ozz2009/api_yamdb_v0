"""Админка приложения Reviews."""

from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title, User


class TitleAdmin(admin.ModelAdmin):
    """Админка модели Titles."""

    list_display = ('pk', 'name', 'year', 'description', 'category')
    search_fields = ('name',)
    list_filter = ('id',)
    empty_value_display = '-пусто-'


class ReviewAdmin(admin.ModelAdmin):
    """Админка модели Review."""

    list_display = ('pk', 'title_id', 'text', 'author', 'score', 'pub_date')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


admin.site.register(Title, TitleAdmin)
admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment)
admin.site.register(User)
