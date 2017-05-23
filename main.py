# coding: utf-8

import os
import json
import time
import requests
from bs4 import BeautifulSoup, NavigableString, Tag

url_base = "http://www.reuters.com"
url_wire = url_base + "/assets/jsonWireNews"

dir_articles = "articles/"

wait = 60.0

finished = []

if not os.path.isdir(dir_articles):
    os.makedirs(dir_articles)
    print("Created directory ", dir_articles)

def find_keywords(soup):
    kw = soup.find("meta", {"name":"keywords"})['content'].split(",")
    return kw

def save_article(h):
    url = url_base + h['url']
    id_a = h['id']
    
    filename = id_a + ".json"
    path = dir_articles + filename
    h['filename'] = filename

    art = requests.get(url)
    soup = BeautifulSoup(art.content, "lxml")
    
    text = ""
    for c in soup.find(id="article-text"):
        if isinstance(c, Tag):
            if not c.string == None:
                text = text + c.string + "\n"
    
    h['text'] = text
    
    h['keywords'] = find_keywords(soup)
    ms = int(h['dateMillis'])
    h['datetime'] = str(datetime.datetime.fromtimestamp(ms/1000.0))

    with open(path, 'w') as f:
        json.dump(h, f)

    print_h(h)

def print_h(h):

    print("###################################################################")
    print("headline:", h['headline'])
    print("datetime: ", h['datetime'])
    print("ID:", h['id'])
    print("URL:", h['url'])
    print("filename:", h['filename'])
    print("keywords:", h['keywords'])
    print("TEXT:")
    print(h['text'])

def load_article(path):
    with open(path) as f:
        article = json.load(f)


t_start = time.time()
while True:
    r_wire = requests.get(url_wire)
    headlines = r_wire.json()['headlines']
    
    for h in headlines:
        if h['id'] not in finished:
            try:
                save_article(h)
                finished.append(h['id'])
            except TypeError:
                print("Failed parsing headline")
                print(h)
                print(h, file=open("errors_TypeError.txt", "a"))
            except KeyboardInterrupt:
                print("KeyboardInterrupt")
                raise
            except:
                print("Something unseen wen't wrong")
                print(h, file=open("errors_other.txt", "a"))


    time.sleep(wait - ((time.time() - t_start) % wait))
    

