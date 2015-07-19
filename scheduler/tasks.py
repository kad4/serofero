import time

import requests
from celery import shared_task

from sf.models import Article
from classifier.classifier import NepClassifier
from .parser import RSSParser

@shared_task
def obtain_articles():
    parser = RSSParser()
    print('Parsing RSS')
    articles = parser.get_articles()

    clf = NepClassifier()
    clf.load_data()
    clf.load_clf()

    for article in articles:
        category = clf.predict(article['content'])
        print(article['link'],' ',category)

        obj = Article.objects.create(
            url = article['link'],
            title = article['title'],
            content = article['content'][:300],
            img_url = article['img_url'],
            category = category
        )

        # Download and save image
        obj.get_remote_img()
        
        obj.save()
