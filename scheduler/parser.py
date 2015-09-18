import requests
from bs4 import BeautifulSoup


class RSSParser():
    def __init__(self, urls):
        # List of urls to parse
        self.urls = urls

    def get_articles(self):
        articles = []
        for url in self.urls:
            print('Current URL: ', url)

            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:12.0)'
                + ' Gecko/20100101 Firefox/21.0'
            }

            r = requests.get(url, headers=headers)
            # r.encoding = 'utf-8'
            content = r.text

            soup = BeautifulSoup(content, 'xml')
            items = soup.find_all('item')

            for item in items:
                link = item.link.string

                article = {
                    'title': item.title.string,
                    'link': link,
                }

                articles.append(article)
        return(articles)
