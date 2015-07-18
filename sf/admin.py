from django.contrib import admin
from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'content', 'url', 'views')

admin.site.register(Article,ArticleAdmin)
