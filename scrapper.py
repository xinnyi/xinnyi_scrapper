import requests
import re
from lxml import html
from lxml import etree
from urllib.parse import urlparse
import argparse


parser = argparse.ArgumentParser(description='save articles')
parser.add_argument("-u", "--url", help="url of the article to be saved",
                    default="https://www.20min.ch/story/mir-als-finanzminister-ist-es-nicht-mehr-wohl-in-meiner-haut-733321798843")
args = parser.parse_args()


def elementToText(element):
    text = element.text
    if text is None:
        text = ""


def printArticles(articles):
    for article in articles:
        print(etree.tostring(article, pretty_print=True))
    return


def printBody(tree):
    print(etree.tostring(tree, pretty_print=True))
    return


def printContent(tree):
    articles = tree.xpath('//article')
    if len(articles) > 0:
        printArticles(articles)
    else:
        printBody(tree)
    return


def switch(netloc, tree):
    if re.search("^www.wikipedia", netloc) is not None:
        printContent(tree)
    else:
        printContent(tree)
    return


response = requests.get(args.url)
tree = html.fromstring(response.content)

netloc = urlparse(args.url).netloc
switch(netloc, tree)
