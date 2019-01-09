# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

import codecs
import json
import os
import requests


# Web Crawler
class RedditWebCrawler(object):

    REDDIT_URL = 'https://www.reddit.com'

    """docstring for RedditWebCrawler"""
    # def __init__(self, cmdline=None):


    def parse_articles(self, board, path='.', timeout=15):
        filename = board + '.json'
        filename = os.path.join(path, filename)
        print('Processing:')
        headers = {'User-agent': 'Mozilla/5.0'}
        resp = requests.get(
            url = self.REDDIT_URL + '/search?q=' + board,
            timeout=timeout, headers=headers
        )

        soup = BeautifulSoup(resp.text, 'lxml')
        # print(soup.text)

        articles = list()
        for scrollerItem in soup.select('.scrollerItem div div div div'):
            if scrollerItem.find(name='span'):
                if scrollerItem.find(name='span').find(name='a'):
                    article_content = scrollerItem.find(name='span').find(name='a')
                    article = dict()
                    article['name'] = article_content.find(name='span').get_text()
                    article['link'] = self.REDDIT_URL + article_content['href']
                    if len(scrollerItem.find_all(name='a')) > 1:
                        if 'jpg' in scrollerItem.find_all(name='a')[1]['href'] or 'png' in scrollerItem.find_all(name='a')[1]['href']:
                            article['picture_url'] = scrollerItem.find_all(name='a')[1]['href']
                        else:
                            article['picture_url'] = ''
                    else:
                        article['picture_url'] = ''
                    articles.append(article)

        return articles

    # def parse_article(self, link, board):

    @staticmethod
    def store(filename, data, mode):
        with codecs.open(filename, mode, encoding='utf-8') as f:
            f.write(data)

    @staticmethod
    def get(filename, mode='r'):
        with codecs.open(filename, mode, encoding='utf-8') as f:
            return json.load(f)




