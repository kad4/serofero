import time

import requests
from celery import shared_task

from sf.models import Article
from .parser import RSSParser
from .extractor import get_article

from classifier.NepClassifier import NepClassifier

@shared_task
def obtain_articles():
    urls = [
        'http://www.onlinekhabar.com/rss',
        # 'http://www.setopati.com/rss',
        # 'http://www.ratopati.com/rss',
    ]

    parser = RSSParser(urls)
    print('Parsing RSS')
    articles = parser.get_articles()

    clf = NepClassifier()
    clf.load_corpus_info()
    clf.load_clf()

    for article in articles:
        title = article['title']
        link = article['link']
        content, img_url = get_article(link, img = True)

        if(content == ''):
            continue

        # Search if the article already exits
        obj, c_flag = Article.objects.get_or_create(title = title)

        # New object is created
        if(c_flag):
            category = clf.predict(content)
            print(link,' ',category)

            obj.url = link
            obj.title = title
            obj.content = content
            obj.img_url = img_url
            obj.category = category

            # Download and save image
            obj.get_remote_img()
            
            obj.save()
