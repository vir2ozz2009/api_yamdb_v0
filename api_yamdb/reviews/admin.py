from django.contrib import admin

from .models import Categories, Genres, Review, Titles, User


class TitlesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'description', 'category')
    search_fields = ('name',)
    list_filter = ('id',)
    empty_value_display = '-пусто-'


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'text', 'author')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


admin.site.register(Titles, TitlesAdmin)
admin.site.register(Genres)
admin.site.register(Categories)
admin.site.register(Review, ReviewAdmin)
admin.site.register(User)
