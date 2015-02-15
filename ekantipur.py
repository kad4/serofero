import os
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup

import extractor

categories=[{'name':'business','value':2,'page':31},
            {'name':'sports','value':3,'page':23},
            {'name':'news','value':10,'page':1}]

for category in categories:
    
    #Directory to store articles
    base_path='ekantipur/'+category['name']
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    
    base_url="http://www.ekantipur.com/np/category/{0}/page/{1}/"

    while(True):
        #Format for the url containig articles list
        url=base_url.format(category['value'],category['page'])
        print('\nCurrent Page: ',url)

        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.ConnectionError:
            print('Network Error')
            break
        except requests.exceptions.HTTPError:
            print('Server Error')
            break
        else:
            # Extract link for articles
            soup=BeautifulSoup(response.text)
            links=soup.select("h6 > a")
            if(len(links)==0):
                break

            for link in links:
                print('URL: ',link['href'])

                # Parsing the url
                parseurl=urlparse(link['href'])

                filename=parseurl.path.split('/')[6].split('.')[0]+".txt"
                filepath=base_path+'/'+filename

                # Checking if the file exists
                if (not(os.path.isfile(filepath))):
                    content=extractor.getContent(link['href'])

                    # Saving content to file
                    if(content):
                        file=open(filepath,'w')
                        file.write(content)
                        file.close()
        category['page']=category['page']+1
