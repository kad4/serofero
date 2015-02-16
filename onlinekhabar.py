import os
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup

import extractor

categories=[{'name':'ent-news','page':1},
            {'name':'bank','page':1},
            {'name':'tourism','page':1},
            {'name':'rojgar','page':1},
            {'name':'auto','page':1},
            {'name':'sports','page':1},
            {'name':'news','page':1},]

for category in categories:

    # Directories to store articles 
    base_path='onlinekhabar/'+category['name']
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    
    base_url="http://www.onlinekhabar.com/category/{0}/page/{1}/"

    while(True):
        # Format for the url containing articles list
        url=base_url.format(category['name'],category['page'])
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
            soup=BeautifulSoup(response.text).find(id='sing_left')
            links=soup.find_all('a',rel='bookmark')
            for link in links:
                print('URL: ',link['href'])

                # Parsing the url
                parseurl=urlparse(link['href'])

                filename=parseurl.path.split('/')[3]+".txt"
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
