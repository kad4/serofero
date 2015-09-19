import json

from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from sf.models import Article


def get_articles(category):
    articles = Article.objects.filter(category=category)\
        .order_by('-pub_date')

    if(len(articles) == 0):
        return([], None)

    for i in range(len(articles)):
        articles[i].content = articles[i].content[:300]

    first_article = articles[0]
    articles = articles[1:6]

    return(articles, first_article)


def index(request):
    articles = Article.objects.all().order_by('-pub_date').order_by('-image')[:30]

    for i, article in enumerate(articles):
        articles[i].content = articles[i].content[:300]

        articles_list = []
        ids = json.loads(article.similar_articles)[:3]

        for id in ids:
            try:
                similar_article = Article.objects.get(pk=id)
                articles_list.append(similar_article)
            except ObjectDoesNotExist:
                pass

        articles[i].articles_list = articles_list

    first_article = articles[0]
    articles = articles[1:]

    content_dict = {
        'articles': articles,
        'first_article': first_article,
        'popular': articles[:5]
    }

    return render(request, 'sf/index.html', content_dict)


def category(request, category='news'):
    articles = Article.objects.filter(category=category).order_by('-pub_date')

    for i, __ in enumerate(articles):
        articles[i].content = articles[i].content[:300]

    content_dict = {
        'category_name': category,
        'articles': articles,
    }
    return render(request, 'sf/category.html', content_dict)
