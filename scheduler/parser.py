import requests
from bs4 import BeautifulSoup

from . import extractor

class RSSParser():
    def __init__(self,url = ''):
        if(url == ''):
            self.urls = [
                'http://www.onlinekhabar.com/rss',
                # 'http://www.setopati.com/rss',
                # 'http://www.ratopati.com/rss',
            ]
        else:
            self.urls = [url]

    def get_articles(self):
        articles = []
        for url in self.urls:
            print('Current URL: ',url)
            r = requests.get(url)
            content = r.text

            soup = BeautifulSoup(content, 'xml')
            items = soup.find_all('item')

            items = items[:3]
            for item in items:
                link = item.link.string
                content, img_url = extractor.get_article(
                    url = link, img = True
                )

                article={
                    'title' : item.title.string,
                    'date' : item.pubDate.string,
                    'link' : link,
                    'content' : content,
                    'img_url' : img_url
                }

                articles.append(article)
        return(articles)
