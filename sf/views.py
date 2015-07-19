from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404

from .models import Article

def index(request):
	news = Article.objects.filter(category = 'news').order_by('-pub_date')[:6]
	news_first = news[0]
	news = news[1:6]

	politics = Article.objects.filter(category = 'politics')[:6]
	politics_first = politics[0]
	politics = politics[1:6]

	content_dict = {
		'news' : news,
		'news_first' : news_first,

		'politics' : politics,
		'politics_first' : politics_first,

		'business' : politics,
		'business_first' : politics_first,

		'sports' : politics,
		'sports_first' : politics_first,

		'entertain' : politics,
		'entertain_first' : politics_first,

		'popular' : news,
	}

	return render(request, 'sf/index.html', content_dict)

def category(request, category = 'news'):
	articles = Article.objects.filter(category = category).order_by('-pub_date')

	content_dict = {
		'category_name' : category,
		'articles' : articles,
	}
	return render(request, 'sf/category.html', content_dict)
