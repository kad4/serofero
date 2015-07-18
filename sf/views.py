from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404

from .models import Article

def index(request):
	news = Article.objects.filter(category = 'news')[:6]
	news_first = news[0]
	news = news[1:6]

	politics = Article.objects.filter(category = 'politics')[:6]
	politics_first = politics[0]
	politics = politics[1:6]

	content_dict = {
		'news_first' : news_first,
		'news' : news,

		'politics' : politics,
		'politics_first' : politics_first,
	}

	return render(request, 'sf/index.html', content_dict)
