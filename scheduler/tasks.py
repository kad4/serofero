import json

import numpy as np
from numpy.linalg import norm
from celery import shared_task

from sf.models import Article
from .parser import RSSParser
from .extractor import get_article

from NepClassifier.NepClassifier import NepClassifier
from NepClassifier.NepClassifier import TfidfVectorizer


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
    clf.load_clf()

    print("Extracting articles")
    for article in articles:
        title = article['title']
        link = article['link']
        content, img_url = get_article(link, img=True)

        if(content == ''):
            continue

        # Search if the article already exits
        obj, c_flag = Article.objects.get_or_create(title=title)

        # New object is created
        if(c_flag):
            category = clf.predict(content)
            print(link, ' ', category)

            obj.url = link
            obj.title = title
            obj.content = content
            obj.img_url = img_url
            obj.category = category

            # Download and save image
            obj.get_remote_img()

            obj.save()

    print("Calculating similar articles")

    vectorizer = TfidfVectorizer(max_stems=10000)
    vectorizer.load_corpus_info()

    # Find alternative
    articles = Article.objects.all()
    new_articles = Article.objects.filter(similar_articles='')

    for article in new_articles:
        article_vector = vectorizer.tf_idf_vector(article.content)
        similar_articles = []

        for item in articles:
            if(item.id == article.id):
                continue

            item_vector = vectorizer.tf_idf_vector(item.content)
            similarity_cof = np.dot(article_vector, item_vector) \
                / (norm(article_vector) * norm(item_vector))

            if(similarity_cof >= 0.9999):
                print(similarity_cof)
                similar_articles.append(item.id)

        article.similar_articles = json.dumps(similar_articles)
        article.save()
