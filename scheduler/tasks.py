from celery import shared_task

from .parser import rssparser

@shared_task
def obtainArticles():
	print('YOLO')
	return
	parser=rssparser()
	articles=parser.getArticles()