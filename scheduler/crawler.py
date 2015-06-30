import sys
import os
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup

import extractor

if (__name__=='__main__'):
    if(len(sys.argv)!=2):
        print('No argument given')
        sys.exit(0)
    else:
        site_str=sys.argv[1]
        site=[False,False,False,False]
        if(site_str=='onlinekhabar'):
            site[0]=True
        elif(site_str=='ekantipur'):
            site[1]=True
        elif(site_str=='setopati'):
            site[2]=True
        elif(site_str=='nagariknews'):
            site[3]=True
        else:
            print('Wrong site entered')
            sys.exit(0)

        categories=[]
        base_path=''
        
        # Categories for individual sites
        if(site[0]):
            categories=[
                {'name':'technology','page':1},
                {'name':'ent-news','page':1},
                {'name':'bank','page':1},
                {'name':'tourism','page':1},
                {'name':'rojgar','page':1},
                {'name':'auto','page':1},
                {'name':'sports','page':1},
                {'name':'news','page':1},
                ]

        elif(site[1]):
            categories=[
                {'name':'world','value':27,'page':1},
                {'name':'business','value':2,'page':1},
                {'name':'sports','value':3,'page':1},
                {'name':'news','value':10,'page':1},
                ]

        elif(site[2]):
            categories=[
                {'name':'bajar','page':1,'maxpage':29},
                {'name':'khel','page':1,'maxpage':39},
                {'name':'samaj','page':1,'maxpage':185},
                {'name':'raajneeti','page':1,'maxpage':286},
                ]
        
        elif(site[3]):
            categories=[
                {'name':'health','page':0,'maxpage':10,'skip':14},
                {'name':'world','page':0,'maxpage':63,'skip':14},
                {'name':'sports','page':0,'maxpage':272,'skip':14},
                {'name':'economy','page':0,'maxpage':288,'skip':14},
                {'name':'politics','page':0,'maxpage':481,'skip':14},
                {'name':'entertainment','page':0,'maxpage':571,'skip':9},
                {'name':'society','page':0,'maxpage':571,'skip':14},
                ]

    for category in categories:

        # Directories to store articles
        base_path=site_str+'/'+category['name']
        if not os.path.exists(base_path):
            os.makedirs(base_path)
        
        base_url=''
        
        if(site[0]):
            base_url='http://www.onlinekhabar.com/category/{0}/page/{1}/'
        elif(site[1]):
            base_url='http://www.ekantipur.com/np/category/{0}/page/{1}/'
        elif(site[2]):
            base_url='http://www.setopati.com/{0}/page/{1}/'
        elif(site[3]):
            base_url='http://www.nagariknews.com/{0}.html?start={1}'
        
        while(True):
            # Format for the url containing articles list
            url=''

            if(site[0]):
                url=base_url.format(category['name'],category['page'])
            elif(site[1]):
                url=base_url.format(category['value'],category['page'])
            elif(site[2]):
                url=base_url.format(category['name'],category['page'])
            elif(site[3]):
                url=base_url.format(category['name'],category['page']*category['skip'])

            print('\nCurrent Page: ',url)

            try:
                # User-agent to use
                user_agent = {'User-agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0'}
                response  = requests.get(url, headers = user_agent)
                response.encoding = 'utf-8'
                response.raise_for_status()
            except requests.exceptions.ConnectionError:
                print('Network Error')
                break
            except requests.exceptions.HTTPError:
                print('Server Error')
                break
            else:
                soup=None
                links=None
                
                # Extracting links from current page
                if(site[0]):
                    soup=BeautifulSoup(response.text).find(id='sing_left')
                    links=soup.find_all('a',rel='bookmark')
                elif(site[1]):
                    soup=BeautifulSoup(response.text)
                    links=soup.select('h6 > a')
                elif(site[2]):
                    soup=BeautifulSoup(response.text).find('ul',class_='news_list')
                    links=list(set(soup.select('li > a')))
                elif(site[3]):
                    soup=BeautifulSoup(response.text).find('div',class_='itemList')
                    links=soup.select('h1 > a')
                    for link in links:
                        link['href']='http://www.nagariknews.com'+link['href']
                
                # Break if no links are found
                if(not(links)):
                    break
                
                # Visit individual links
                for link in links:
                    print('URL: ',link['href'])

                    # Parsing the url
                    parseurl=urlparse(link['href'])
                   
                    # Getting file name for article
                    filename=''
                    if(site[0]):
                        filename=parseurl.path.split('/')[-2]+'.txt'
                    elif(site[1]):
                        filename=parseurl.path.split('/')[-1].split('.')[0]+'.txt'
                    elif(site[2]):
                        filename=parseurl.path.split('/')[-2]+'.txt'
                    elif(site[3]):
                        filename=parseurl.path.split('/')[-1].split('.')[0]+'.txt'

                    filepath=base_path+'/'+filename

                    # Checking if the file exists
                    if (not(os.path.isfile(filepath))):
                        content=extractor.getArticle(link['href'])[0]

                        # Saving content to file
                        if(content):
                            file=open(filepath,encoding='utf-8',mode='w')
                            file.write(content)
                            file.close()

            # Increase the page count
            category['page']=category['page']+1

            if(site[2] or site[3]):
                if(category['page']>category['maxpage']):
                    break;

