import requests
import re
import uuid
from lxml import html, etree
from urllib.parse import urlparse
from datetime import datetime
from elasticsearch import Elasticsearch
import argparse

# Convert lxml element to string
def elementToText(element):
    if element.tag in ['button', 'input', 'script']:
        return ''
    text = str(element.text or "")
    if text is None:
        text = ""
    if element.tag in ['img', 'svg']:
        text = "[Image]\n"
    elif element.tag in ['h1', 'h2', 'h3', 'h4', 'h5']:
        text = "<b>" + text + "<b>\n"
    elif element.tag in ['a']:
        link = element.get("href")
        text = "<i>" + text + " " + str(element.get("href") or "") + "</i>"
    elif element.tag in ['div', 'p']:
        text = text + "\n"
    for child in element.getchildren():
        text += elementToText(child)
    return text

# Saves a string to elasticsearch
def saveToElastic(text):
    doc = {
        'url': args.url,
        'text': text,
        'timestamp': datetime.now(),
    }
    id = uuid.uuid4()
    res = es.index(index="test-index", id=id, body=doc)
    print(res['result'], id)


# default
def handleWebsite():
    articles = body.xpath('//article')
    if len(articles) > 0:
        text = ''
        for article in articles:
            text += elementToText(article) + '\n'
        saveToElastic(text)
    else:
        saveToElastic(elementToText(body))

    return


def handleWikipedia():
    print("wikipedia.org/...")

def handleNoseryoung():
    print("noseryoung.ch")

# Decide wich method should be used
def switch(netloc):
    for k, v in netLocations.items():
        if re.search(k, netloc) is not None:
            v()
            return
    handleWebsite()
    return


# Parse arguments
parser = argparse.ArgumentParser(description='save articles')
parser.add_argument("-u", "--url", help="url of the article to be saved", default="https://www.20min.ch/story/mir-als-finanzminister-ist-es-nicht-mehr-wohl-in-meiner-haut-733321798843")
args = parser.parse_args()

# Connect to elasticseatch
es = Elasticsearch(["localhost:9200"])


# Define locations wich are handled differently
netLocations = {"wikipedia.org": handleWikipedia,
                "noseryoung.ch": handleNoseryoung}


# Make request
response = requests.get(args.url)

# Parse response
tree = html.fromstring(
    response.content, parser=etree.HTMLParser(remove_comments=True))
body = tree.xpath('//body')[0]

# Handle response
switch(urlparse(args.url).netloc)
