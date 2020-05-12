import requests
import re
import pika
import os
import uuid
import json
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
        text = "[%s]\r\n" % element.get("alt")
    elif element.tag in ['video']:
        text = "[video]"
    elif element.tag in ['a']:
        link = element.get("href")
        text = "<i>" + text + " " + str(element.get("href") or "") + "</i>"
    for child in element.getchildren():
        text += elementToText(child)
    if element.tag in ['h1', 'h2', 'h3', 'h4', 'h5']:
        text = "\r\n<b>" + text + "</b>\r\n"
    if element.tag in ['div', 'p'] and element.text is not None:
        text = text + "\r\n"
    text = re.sub(r'(([\r\n]\s*){3,}?)+', r'\r\n\r\n', text)  # remove multiple linebreaks
    text = re.sub(r'[ \t]{4,}', r'    ', text)  # reduce multiple spaces and tabs
    return text

# create a function which is called on incoming messages
def callback(ch, method, properties, body):
    print(" [x] Received " + body.decode('utf-8'))
    body = json.loads(body)

    try:
        # Make request
        response = requests.get(body['url'])

        # Parse response
        tree = html.fromstring(response.content, parser=etree.HTMLParser(remove_comments=True))

        # Handle response
        articles = tree.xpath('//article')
        if len(articles) > 0:
            text = ''
            for article in articles:
                text += elementToText(article) + '\n'

            # new uuid
            id = uuid.uuid4()

            # query for article with url and userid
            res = es.search(index="article", body={"_source": False, "query": {
                "bool": {"should": [
                    {"term": {"userid": body['userid']}},
                    {"term": {"url": body['url']}}
                ]
                }}})

            # replace id with id of found article
            if res['hits']['total']["value"] == 1:
                id = (res['hits']['hits'][0]["_id"])

            # update or create article
            res = es.index(index="article", id=id, body={
                'url': body['url'],
                'userid': body['userid'],
                'article': text,
                'timestamp': datetime.now()
            })
            print(res['result'], id)
    except Exception as error:
        print(error)


# Connect to elasticseatch
es = Elasticsearch(["klemens.li:9200"])

# Connect to rabbitmq
params = pika.URLParameters("amqp://klemens.li:5672")
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='artistore_articles')


# set up subscription on the queue
channel.basic_consume('artistore_articles', callback, auto_ack=True)

# start consuming (blocks)
channel.start_consuming()
connection.close()
