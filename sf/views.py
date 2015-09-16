from django.shortcuts import render

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
    news, news_first = get_articles('news')
    sports, sports_first = get_articles('sports')
    politics, politics_first = get_articles('politics')
    business, business_first = get_articles('business')
    entertain, entertain_first = get_articles('entertainment')

    content_dict = {
        'news': news,
        'news_first': news_first,

        'politics': politics,
        'politics_first': politics_first,

        'business': business,
        'business_first': business_first,

        'sports': sports,
        'sports_first': sports_first,

        'entertain': entertain,
        'entertain_first': entertain_first,

        'popular': news,
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
