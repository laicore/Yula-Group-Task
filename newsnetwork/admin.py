from django.contrib import admin
from django.utils.html import format_html
from .models import *
# Register your models here.


@admin.register(PostModel)
class PostModeratedAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'author',
                    'moderated', 'addedDatetime', 'open_post']

    def open_post(self, obj):
        return format_html("<a href=\"{url}\">{url}</a>", url=obj.get_url())
