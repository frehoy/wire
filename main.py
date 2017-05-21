import time
import requests
from bs4 import BeautifulSoup, NavigableString, Tag

url_base = "http://www.reuters.com"
url_wire = url_base + "/assets/jsonWireNews"

def print_article(url):
	art = requests.get(url)
	soup = BeautifulSoup(art.content, "lxml")
	
	for c in soup.find(id="article-text"):
		if isinstance(c, Tag):
			if not c.string == None:
				print(c.string)

finished = []
finished_headlines = []

starttime=time.time()
while True:
	print ("tick")
	r_wire = requests.get(url_wire)
	print(r_wire)
	headlines = r_wire.json()['headlines']
	for h in headlines:
		if h['id'] not in finished:
			print("#################################################################################")
			print(h['headline'])
			url_article = url_base + h['url']
			print(url_article)
			print_article(url_article)
			finished.append(h['id'])
			finished_headlines.append(h['headline'])
	time.sleep(60.0 - ((time.time() - starttime) % 60.0))
