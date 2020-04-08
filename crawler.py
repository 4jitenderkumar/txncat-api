import wikipedia
import numpy as np
import fire
import json
import codecs
import pandas as pd
from string import punctuation
# from nltk.corpus import stopwords
from bs4 import BeautifulSoup

def getRetlWebPg(query):
    try: 
        from googlesearch import search 
    except ImportError:  
        print("No module named 'google' found") 
    j=query
    # to search 
    #query = "MAUNGATAPU PHARMACY LT MAUNGATAPU    NZ"
    searchResults=sum(1 for x in search(query + " wiki", tld="com", num=5, stop=1, pause=2))
    print((searchResults))
    if (searchResults)>0:
        for j in search(query + " wiki", tld="com", num=10, stop=1, pause=2): 
            print(j) 
    return(j)
  

from pyquery import PyQuery as pq
import requests
import logging 
from socket import timeout
from urllib.error import HTTPError, URLError


def getURLText(target_url):
    #target_url = "https://www.maungatapupharmacy.co.nz/?sa=X&ved=2ahUKEwiLvYnmlfbmAhU54jgGHZbRD2UQFjAAegQIAhAB"
    #print(target_url)
    respondent=target_url
    #user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36'
    #headers = {'User-Agent': user_agent}
    headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.42 Safari/537.36',
    'x-nba-stats-origin': 'stats',
    }
    try:
        content = requests.get(target_url,verify=False,timeout=10,headers=headers).content
        
    except (HTTPError, URLError) as error:
        logging.error('Data of %s not retrieved because %s\nURL: %s', name, error, url)
    except timeout:
        logging.error('socket timed out - URL %s', url)
    except ConnectionError as e:
        print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
        print(str(e))            
    except Exception as e:
        print("OOPS!! General Error")
        print(str(e))
        #renewIPadress()
    except KeyboardInterrupt:
        print("Someone closed the program")
    else:
        logging.info('Access successful.')
        print(len(content))
        
        if(len(content)>0):
        #print(content)
            doc = pq(content)
            #print(doc)
            respondent = doc('p').text() #+ doc('div').text()  #doc(".formatted_content ul").text()
            if (len(respondent)<20):
                respondent = doc('div').text()
                if (len(respondent)<20):
                    respondent = doc('.formatted_content ul').text()
            #print(len(respondent))


    return(respondent)

def getText(query):
    query = query.replace(' ', '+')
    URL = f"https://google.com/search?q={query}"
    # URL = "https://dilworth.co.nz/bethlehem-tauranga/"
    print(URL)

    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    headers = {"user-agent" : USER_AGENT}

    resp = requests.get(URL, headers = headers)
    print(resp)
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, "html.parser")
        # print(soup)
    else:
        print("Error")    

    results = ""

    for g in soup.find_all('span', class_='st'):
        print(g.text)
        results = results + g.text + " "
  
    print(results)
    # return results    


def getTEST(query):
    query = query.replace(' ', '+')
    URL = f"https://google.com/search?q={query}"
    # URL = "https://dilworth.co.nz/bethlehem-tauranga/"
    print(URL)

    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    headers = {"user-agent" : USER_AGENT}

    resp = requests.get(URL, headers = headers)
    # print(resp)
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, "html.parser")
        # print(soup)
    else:
        print("Error")    

    results = []
    count = 3

    for g in soup.find_all('div', class_='r'):
        if count == 0:
            print('end')
            break

        print("hi")
        # print(g)
        anchors = g.find_all('a')
        # anchors = g.find_all('h3')
        # print(anchors)
        if anchors:
            link = anchors[0]['href']
            title = g.find('h3').text
            # information = g.find('p').text
            print(link)
            # print(title)
            # item = {
            #     "title": title,
            #     "link": link
            #     # "information": information
            # }
            # print(link)
            results.append(link)
            count = count-1    
    print(results)

    output = []    
    for i_URL in results:
        resp = requests.get(i_URL, headers = headers)
        # print(resp)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, "html.parser")
            # print(soup)
        else:
            print("Error")
    
        description = soup.find("meta",  property="og:description")
        title = soup.find("meta",  property="og:title") 
        if description:
            print(description["content"] if description else "No meta title given")
            output.append(description["content"] + " ")
        elif title:
            print(title["content"] if title else "No meta title given")
            output.append(title["content"] + " ")
        else:
            print("NOT FOUND")

    print(output)    



getText("shopify")
# target_url = getRetlWebPg("MAUNGATAPU")
# output = getURLText(target_url) 
# print(output) 