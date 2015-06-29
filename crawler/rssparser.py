from bs4 import BeautifulSoup
import requests

import extractor

class rss_parser():
	def __init__(self,url=''):
		if(url==''):
			self.urls=[
				'http://www.onlinekhabar.com/rss',
				'http://www.setopati.com/rss',
				'http://www.ratopati.com/rss',
			]
		else:
			self.urls=[url]

	def getArticles(self):
		articles=[]
		for url in self.urls:
			r=requests.get(url)
			content=r.text

			soup=BeautifulSoup(content,'xml')
			items=soup.find_all('item')

			items=items[:3]
			for item in items:
				link=item.link.string
				content,img_url=extractor.getArticle(url=link,img=True)[:300]

				# Code for images

				article={
				'title':item.title.string,
				'date':item.pubDate.string,
				'comments':item.comments.string,
				'link':link,
				'content':content
				}

				articles.append(article)
		return(articles)

if __name__ == '__main__':
	parser=rss_parser()
	print(parser.getArticles())