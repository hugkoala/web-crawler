# -*- coding: utf-8 -*-

import codecs
import json
import os
import requests

class RedditWebCrawler(object):


    REDDIT_URL = 'https://www.zhihu.com/'

    """docstring for ZhihuWebCrawler"""
    def __init__(self, cmdline=None):


    def parse_articles(self, board, path='.', timeout=5):
        filename = board + '.json'
        filename = os.path.join(path, filename)
        print('Processing:')
        resp = requests.get(
            url = self.REDDIT_URL + '/topic#' + board,

        )
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