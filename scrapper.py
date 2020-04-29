import requests
import re
from lxml import html, etree
from urllib.parse import urlparse
import argparse


parser = argparse.ArgumentParser(description='save articles')
parser.add_argument("-u", "--url", help="url of the article to be saved",
                    default="https://www.20min.ch/story/mir-als-finanzminister-ist-es-nicht-mehr-wohl-in-meiner-haut-733321798843")
args = parser.parse_args()


def elementToText(element):
    text = ''
    if element.tag not in ['button', 'input', 'script']:
        text = element.text
        if text is None:
            text = ""
        if element.tag in ['img', 'svg']:
            text = "[Image]\n"
        if element.tag in ['h1', 'h2', 'h3', 'h4', 'h5']:
            text = "\n<b>"+text+"<b>\n"
        if element.tag in ['div', 'p']:
            text = text + "\n"
        for child in element.getchildren():
            text += elementToText(child)
    return text


def printArticles(articles):
    for article in articles:
        print(elementToText(article))
    return


def printBody(body):
    print(elementToText(body))
    return


def printContent(body):
    articles = body.xpath('//article')
    if len(articles) > 0:
        printArticles(articles)
    else:
        printBody(body)
    return


def switch(netloc, body):
    if re.search("^www.wikipedia", netloc) is not None:
        printContent(body)
    else:
        printContent(body)
    return


response = requests.get(args.url)
tree = html.fromstring(
    response.content, parser=etree.HTMLParser(remove_comments=True))
netloc = urlparse(args.url).netloc
switch(netloc, tree.xpath('//body')[0])
