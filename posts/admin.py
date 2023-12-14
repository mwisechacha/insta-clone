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

    class Media:
        css = {
            'all':['posts/styles.css']
        }

admin.site.register(Like)
admin.site.register(Follow)
admin.site.register(Comment)
