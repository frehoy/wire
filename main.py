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

def save_article(h):
    url = url_base + h['url']
    id_a = h['id']
    
    filename = "article_" + id_a + ".json"
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

    with open(path, 'w') as f:
        json.dump(h, f)

    print_h(h)

def print_h(h):

    print("###################################################################")
    print("headline:", h['headline'])

    print("ID:", h['id'])
    print("URL:", h['url'])
    print("filename:", h['filename'])
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
            save_article(h)
            finished.append(h['id'])
    time.sleep(wait - ((time.time() - t_start) % wait))
    

