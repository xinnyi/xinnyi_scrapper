import requests
import re
import pika
import os
import logging
from lxml import html, etree
from urllib.parse import urlparse
from datetime import datetime
from elasticsearch import Elasticsearch


# Convert lxml element to string
def elementToText(element):
    if element.tag in ['button', 'input', 'script']:
        return ''
    text = str(element.text or "")
    if text is None:
        text = ""
    if element.tag in ['img', 'svg']:
        text = "[Image]\r\n"
    elif element.tag in ['h1', 'h2', 'h3', 'h4', 'h5']:
        text = "<b>" + text + "</b>\r\n"
    elif element.tag in ['a']:
        link = element.get("href")
        text = "<i>" + text + " " + str(element.get("href") or "") + "</i>"
    elif element.tag in ['div', 'p'] and element.text is not None:
        text = text + "\r\n"
    for child in element.getchildren():
        text += elementToText(child)
    text = re.sub(r'(([\r\n]\s*){3,}?)+', r'\r\n\r\n', text)
    text = re.sub(r'[ \t]{4,}', r'    ', text)
    text = re.sub(r'(\t\s*){2,}', r'\t', text)
    return text

# Saves an article to elasticsearch
def saveToElastic(url, text):
    doc = {
        'text': text,
        'timestamp': datetime.now(),
    }

    res = es.index(index="scrapper", id=url, body=doc)
    print(res['result'], url)


# default
def handleWebsite(url, body):
    articles = body.xpath('//article')
    if len(articles) > 0:
        text = ''
        for article in articles:
            text += elementToText(article) + '\n'
        saveToElastic(url, text)
    else:
        saveToElastic(url, elementToText(body))


def handleWikipedia(url, body):
    print("wikipedia.org/...")

def handleNoseryoung(url, body):
    print("noseryoung.ch")

# Decide wich method should be used
def switch(url, body):
    for k, v in netLocations.items():
        if re.search(k, urlparse(url).netloc) is not None:
            v(url, body)
            return
    handleWebsite(url, body)


# create a function which is called on incoming messages
def callback(ch, method, properties, body):
    print(" [x] Received " + body.decode('utf-8'))
    url = body.decode('utf-8')
    try:
        # Make request
        response = requests.get(url)

        # Parse response
        tree = html.fromstring(response.content, parser=etree.HTMLParser(remove_comments=True))
        body = tree.xpath('//body')[0]

        # Handle response
        switch(url, body)
    except requests.exceptions.RequestException as error:
        print(error)


# Define locations wich are handled individullay
netLocations = {"wikipedia.org": handleWikipedia,
                "noseryoung.ch": handleNoseryoung}


# Connect to elasticseatch
es = Elasticsearch(["localhost:9200"])

# Connect to rabbitmq
params = pika.URLParameters("amqp://localhost:5672")
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='scrapper')


# set up subscription on the queue
channel.basic_consume('scrapper', callback, auto_ack=True)

# start consuming (blocks)
channel.start_consuming()
connection.close()
