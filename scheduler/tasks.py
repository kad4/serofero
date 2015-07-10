import time

import requests
from celery import shared_task

from sf.models import Page,Category
from classifier import classifier
from .parser import RSSParser

@shared_task
def obtain_articles():
	parser=rssparser()
	articles=parser.get_articles()

	nep_classifer=classifier.NepClassifier()
	nep_classifer.load_data()

	for article in articles:
		p=Page.objects.create(
			title=article['title'],
			pub_date=time.strptime(article['date'],
                            '%m/%d/%Y %I:%M %p')
			url=article['link'],
			content=article['content'][:300],
			category=None,
		)

		# Download and save image
		p.get_remote_img()
		
		p.save()
