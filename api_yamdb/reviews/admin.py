from django.contrib import admin

from .models import Review, User


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'text', 'author')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


admin.site.register(Review, ReviewAdmin)
