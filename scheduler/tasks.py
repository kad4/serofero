import json
import time

import numpy as np
from numpy.linalg import norm
import requests
from celery import shared_task
from django.utils import timezone

from sf.models import Article
from .parser import RSSParser
from .extractor import get_article

from NepClassifier.NepClassifier import NepClassifier

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

    article_ids = []
    
    print("Extracting articles")
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

            article_ids.append(obj.id)

    print("Calculating similar articles")

    now = timezone.now()
    day = now.day

    article_ids = [51, 52, 53, 54, 55, 56, 57, 58, 59]

    articles = Article.objects.filter(pub_date__day = day)
    for article_id in article_ids:
        article = Article.objects.get(pk = article_id)

        article_vector = clf.tf_idf_vector(article.content)
        similar_articles = []
        
        for item in articles:
            if(item.id == article.id):
                continue

            item_vector = clf.tf_idf_vector(item.content)
            similarity_cof = np.dot(article_vector, item_vector) / (norm(article_vector) * norm(item_vector))

            print(similarity_cof)

            if(similarity_cof >= 0.9):
                similar_articles.append(item.id)

        article.similar_articles = json.dumps(similar_articles) 
        article.save()

