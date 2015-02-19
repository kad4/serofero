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
        site=[False,False,False]
        if(site_str=='onlinekhabar'):
            site[0]=True
        elif(site_str=='ekantipur'):
            site[1]=True
        elif(site_str=='setopati'):
            site[2]=True
        else:
            print('Wrong site entered')
            sys.exit(0)

        categories=[]
        base_path=''
        
        # Categories for individual sites
        if(site[0]):
            categories=[{'name':'technology','page':1},
                {'name':'ent-news','page':1},
                {'name':'bank','page':1},
                {'name':'tourism','page':1},
                {'name':'rojgar','page':1},
                {'name':'auto','page':1},
                {'name':'sports','page':1},
                {'name':'news','page':1},]

        elif(site[1]):
            categories=[{'name':'world','value':27,'page':1},
                {'name':'business','value':2,'page':1},
                {'name':'sports','value':3,'page':1},
                {'name':'news','value':10,'page':1}]

        elif(site[2]):
            categories=[{'name':'raajneeti','page':1},
                {'name':'samaj','page':1},
                {'name':'bajar','page':1},
                {'name':'khel','page':1},]

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
        
        while(True):
            # Format for the url containing articles list
            url=''

            if(site[0]):
                url=base_url.format(category['name'],category['page'])
            elif(site[1]):
                url=base_url.format(category['value'],category['page'])
            elif(site[2]):
                url=base_url.format(category['name'],category['page'])

            print('\nCurrent Page: ',url)

            try:
                response  = requests.get(url, headers={'User-agent': 'Mozilla/5.0'})
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
                
                # Break if no links are found
                if(len(links)==0):
                    break
                
                # Visit individual links
                for link in links:
                    print('URL: ',link['href'])

                    # Parsing the url
                    parseurl=urlparse(link['href'])
                   
                    # Getting file name for article
                    filename=''
                    if(site[0]):
                        filename=parseurl.path.split('/')[3]+'.txt'
                    elif(site[1]):
                        filename=parseurl.path.split('/')[6].split('.')[0]+'.txt'
                    elif(site[2]):
                        filename=parseurl.path.split('/')[2]+'.txt'

                    filepath=base_path+'/'+filename

                    # Checking if the file exists
                    if (not(os.path.isfile(filepath))):
                        content=extractor.getContent(link['href'])

                        # Saving content to file
                        if(content):
                            file=open(filepath,encoding='utf-8',mode='w')
                            file.write(content)
                            file.close()

            # Increase the page count
            category['page']=category['page']+1
