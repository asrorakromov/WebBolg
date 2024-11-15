from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Movie, Comments, Profile, Ip

admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(Ip)


@admin.register(Movie)
class MoviesAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_views', 'likes', 'category', 'get_photo')
    list_filter = ('category',)

    def get_photo(self, obj):
        if obj.photo:
            try:
                return mark_safe(f'<img src="{obj.photo.url}" width="150px">')
            except:
                return '-'

        else:
            return '-'


@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'movie', 'created_at')
    list_filter = ('movie', 'created_at')
    list_display_links = ('id', 'user')
