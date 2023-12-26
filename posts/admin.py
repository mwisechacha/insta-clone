from typing import Any
from django.contrib import admin
from django.utils.html import format_html
from . import models
from .models import Like, Comment
from .admin_mixin import PrepopulateAndDisableUserMixin

# Register your models here.

class PostImageInline(admin.TabularInline):
    model = models.PostImage
    readonly_fields = ['thumbnail']

    def thumbnail(self, instance):
        if instance.image.name != '':
            return format_html(f'<img src="{instance.image.url}" class="thumbnail"/>')
        return ''

@admin.register(models.Post)
class PostAdmin(PrepopulateAndDisableUserMixin, admin.ModelAdmin):
    list_per_page = 10
    inlines = [PostImageInline]

    class Media:
        css = {
            'all':['posts/styles.css']
        }

@admin.register(models.Comment)
class CommentAdmin(PrepopulateAndDisableUserMixin, admin.ModelAdmin):
    list_per_page = 10
    
    
@admin.register(models.Like)
class LikeAdmin(PrepopulateAndDisableUserMixin, admin.ModelAdmin):
    list_per_page = 10



