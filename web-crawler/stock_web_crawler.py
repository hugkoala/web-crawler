# -*- coding: utf-8 -*-

import requests, time, codecs, json, os


class StockWebCrawler(object):

    STOCK_URL = 'http://www.twse.com.tw/exchangeReport/MI_INDEX'

    def __init__(self):
        self.__date = time.strftime('%Y%m%d', time.localtime())

    def get_date(self):
        return self.__date

    def set_date(self, date):
        self.__date = date

    def get_datas(self, path='.'):
        filename = 'stock_' + self.get_date() + '.json'
        filename = os.path.join(path, filename)

        headers = dict()
        headers['response'] = 'json'
        headers['date'] = self.get_date()
        headers['type'] = 'ALL'
        response = requests.get(self.STOCK_URL, headers=headers)
        self.store(filename, response.text, 'w')

    def parse_datas(self, path='.'):
        filename = 'stock_' + self.get_date() + '.json'
        filename = os.path.join(path, filename)
        file = self.get(filename)
        print(file['params'])

    @staticmethod
    def store(filename, data, mode):
        with codecs.open(filename, mode, encoding='utf-8') as f:
            f.write(data)

    @staticmethod
    def get(filename, mode='r'):
        with codecs.open(filename, mode, encoding='utf-8') as f:
            return json.load(f)


if __name__ == '__main__':
    s = StockWebCrawler()
    s.parse_datas()

