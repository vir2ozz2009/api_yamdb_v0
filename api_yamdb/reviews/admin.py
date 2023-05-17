from django.contrib import admin

from .models import Genres, Categories, Titles


class TitlesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'description', 'category')
    search_fields = ('name',)
    list_filter = ('id',)
    empty_value_display = '-пусто-'


admin.site.register(Titles, TitlesAdmin)
admin.site.register(Genres)
admin.site.register(Categories)

# class CategoriesAdmin(admin.ModelAdmin):
#     list_display = ('pk', 'name')
#     search_fields = ('name',)
#     list_filter = ('id',)
#     empty_value_display = '-пусто-'
