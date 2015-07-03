from celery import shared_task

from .parser import rssparser

@shared_task
def obtainArticles():
	parser=rssparser()
	articles=parser.getArticles()