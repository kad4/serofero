from bs4 import BeautifulSoup

import requests

from urllib.parse import urlparse

def getContent(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        print('Network Error')
        return
    except requests.exceptions.HTTPError:
        print('Server Error')
        return
    else:
        soup=BeautifulSoup(response.text)
        parsedURL=urlparse(url)

        # Format to use
        if(parsedURL.netloc=="www.onlinekhabar.com"):
            soup=soup.find('div',id='sing_left')
            soup.find('div',id='comments').decompose()
            paragraphs=soup.find_all('p')
            content=""
            for item in paragraphs:
                if (item.string):
                    content=content+item.string
            return (content)

        if(parsedURL.netloc=="www.ekantipur.com"):
            paragraphs=soup.find("div",class_="newsContentWrapper").find_all('p')
            content=""
            for item in paragraphs:
                if (item.string):
                    content=content+item.string
            return (content)

if __name__ == '__main__':
    print(getContent('http://www.ekantipur.com/np/2071/9/25/full-story/401764.html'))
