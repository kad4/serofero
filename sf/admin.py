from django.contrib import admin
from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'title',
        'category',
        'content',
        'url',
        'views',
        'similar_articles',
        'img_url'
    )

admin.site.register(Article, ArticleAdmin)
