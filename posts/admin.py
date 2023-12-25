from typing import Any
from django.contrib import admin
from django.utils.html import format_html
from . import models
from .models import Like, Follow, Comment

# Register your models here.
class PostImageInline(admin.TabularInline):
    model = models.PostImage
    readonly_fields = ['thumbnail']

    def thumbnail(self, instance):
        if instance.image.name != '':
            return format_html(f'<img src="{instance.image.url}" class="thumbnail"/>')
        return ''

@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_per_page = 10
    inlines = [PostImageInline]

    def get_form(self, request, obj=None, **kwargs):
        form = super(PostAdmin, self).get_form(request, obj, **kwargs)
        if obj is None:
            form.base_fields['user'].initial = request.user
            form.base_fields['user'].disabled = True
        return form
    class Media:
        css = {
            'all':['posts/styles.css']
        }

@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super(CommentAdmin, self).get_form(request, obj, **kwargs)
        if obj is None:
            form.base_fields['user'].initial = request.user
            form.base_fields['user'].disabled = True
        return form
    
    

admin.site.register(Like)
admin.site.register(Follow)

