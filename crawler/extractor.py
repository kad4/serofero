import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup

def getContent(url):
    try:
        response = requests.get(url)
        user_agent = {'User-agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0'}
        response  = requests.get(url, headers = user_agent)
        response.encoding = 'utf-8'
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
        if(parsedURL.netloc=='www.onlinekhabar.com'):
            soup=soup.find('div',id='sing_left')
            soup.find('div',id='comments').decompose()
            paragraphs=soup.find_all('p')
            content=''
            for item in paragraphs:
                if (item.string):
                    content=content+item.string
            return (content)

        elif(parsedURL.netloc=='www.ekantipur.com'):
            soup=soup.find('div',class_='newsContentWrapper')
            paragraphs=soup.find_all('p')
            content=''
            for item in paragraphs:
                if (item.string):
                    content=content+item.string
            return (content)
        
        elif(parsedURL.netloc=='setopati.com'):
           soup=soup.find('div',id='newsbox')
           soup.find('div',class_='fb_like_detail').decompose()
           soup.find('div',class_='comments').decompose()
           paragraphs=soup.find_all('div')+soup.find_all('p')
           content=''
           for item in paragraphs:
                if (item.string):
                    content=content+item.string
           return(content)
        
        elif(parsedURL.netloc=='www.nagariknews.com'):
           soup=soup.find('div',class_="itemFullText")
           content=soup.get_text()
           return(content)

        elif(parsedURL.netloc=='www.ratopati.com'):
            soup=soup.find('div',id='sing_cont')
            paragraphs=soup.find_all('p')
            content=''
            for item in paragraphs:
                if(item.string):
                    content=content+item.string
            return(content)
          
        else:
            print('Match for the site not found')

if __name__ == '__main__':
    print(getContent('http://www.nagariknews.com/health/story/29987.html'))
