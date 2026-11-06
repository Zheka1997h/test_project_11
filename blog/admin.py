from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Настройка админки для блоговых записей"""
    list_display = ('id', 'title', 'created_at', 'is_published', 'views_count')
    list_display_links = ('id', 'title')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)