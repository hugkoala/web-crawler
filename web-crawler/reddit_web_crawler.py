# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

import codecs
import json
import os
import requests

class RedditWebCrawler(object):


    REDDIT_URL = 'https://www.reddit.com/'

    """docstring for RedditWebCrawler"""
    # def __init__(self, cmdline=None):


    def parse_articles(self, board, path='.', timeout=5):
        filename = board + '.json'
        filename = os.path.join(path, filename)
        print('Processing:')
        headers = {'User-agent': 'Mozilla/5.0'}
        resp = requests.get(
            url = self.REDDIT_URL + 'search?q=' + board,
            timeout=timeout, headers=headers
        )

        soup = BeautifulSoup(resp.text, 'lxml')
        # print(soup.text)
        for scrollerItem in soup.select('.scrollerItem div div div div span a'):
            print('----------------------------new----------------------------')
            print(scrollerItem)
            print('----------------------------all----------------------------')
            print(scrollerItem['href'])


        self.store(filename, u'{"articles": [', 'w')

        self.store(filename, u']}', 'a')
        return filename

    # def parse_article(self, link, board):


    @staticmethod
    def store(filename, data, mode):
        with codecs.open(filename, mode, encoding='utf-8') as f:
            f.write(data)

    @staticmethod
    def get(filename, mode='r'):
        with codecs.open(filename, mode, encoding='utf-8') as f:
            return json.load(f)

if __name__ == '__main__':
    r = RedditWebCrawler()
    r.parse_articles(board='Warframe')