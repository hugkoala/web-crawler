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

        params = dict()
        params['response'] = 'json'
        params['date'] = self.get_date()
        params['type'] = 'ALL'
        params['_'] = str(int(time.time() * 1000))
        response = requests.get(self.STOCK_URL, params=params)
        # self.store('tmp.json', response.text, 'w+')
        self.store(filename, self.json_array_to_json_dict(response.text, 'data5'), 'w+')

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

    @staticmethod
    def delete(filename):
        os.remove(filename)

    @staticmethod
    def json_array_to_json_dict(json_str, json_key):
        json_obj = json.loads(json_str)
        results = list()
        for item in json_obj[json_key]:
            result = dict()
            result['STOCK_NO'] = item[0]
            result['STOCK_NM'] = item[1]
            result['TRADING_VOLUME'] = item[2]
            result['NUMBER_OF_TRANSACTIONS'] = item[3]
            result['TURNOVER_IN_VALUE'] = item[4]
            result['OPENING_PRICE'] = item[5]
            result['DAY_HIGH'] = item[6]
            result['DAY_LOW'] = item[7]
            result['CLOSING PRICE'] = item[8]
            result['Dir'] = item[9]
            result['CHANGE'] = item[10]
            result['LAST_BEST_BID_PRICE'] = item[11]
            result['LAST_BEST_BID_VOLUME'] = item[12]
            result['LAST_BEST_ASK_PRICE'] = item[13]
            result['LAST_BEST_ASK_VOLUME'] = item[14]
            results.append(result)

        return json.dumps(results)


if __name__ == '__main__':
    s = StockWebCrawler()
    s.set_date('20190122')
    s.get_datas()
    # s.parse_datas()


