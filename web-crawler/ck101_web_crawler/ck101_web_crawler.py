import requests, logging, time, random;
from bs4 import BeautifulSoup as bs;

BASE_URL = 'https://ck101.com/forum.php?mod=forumdisplay&fid=3419'

type_dict = {0: '', 1: '2399', 2: '2400', 3: '2401', 4: '2402', 5: '2403', 6: '2404', 7: '2405'}
dateline_dict = {0: '', 1: '86400', 2: '172800', 3: '604800', 4: '2592000', 5: '7948800'}
orderby_dict = {0: 'dateline', 1: 'replies', 2: 'views'}


def load_web(url):
    logging.info('===Load Web:{0}==='.format(url))

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4'
    }
    web_res = requests.get(url, headers=headers)
    web_res.encoding = 'utf8'
    time.sleep(random.uniform(0, 2))
    web_bs = bs(web_res, 'lxml')
    return web_bs


def get_all_page_count(web_bs):
    fd_page_bottom = web_bs.find('span', id='fd_page_bottom')
    last_tag = fd_page_bottom.select_one('div').find('a', attrs={'class': 'last'}).text
    return int(last_tag.split(' ')[1])


class CK101WebCrawler(object):
    def __init__(self,
                 novel_type=0,
                 novel_dateline=1,
                 novel_orderby=1,
                 file_dir='.'):
        """

        :param novel_type: 小說型態，預設all
        :param novel_dateline: 小說期限，預設1天
        :param novel_orderby: 小說排序，預設以回覆/查看排序
        :param file_dir: 小說存放路徑，預設以當前執行資料夾
        """
        self.novel_type = novel_type
        self.novel_dateline = novel_dateline
        self.novel_orderby = novel_orderby
        self.file_dir = file_dir

    def get_url_with_args(self):
        url_with_args = BASE_URL
        url_with_args += '&typeid=' + type_dict.get(self.novel_type)
        url_with_args += '&dateline=' + dateline_dict.get(self.novel_dateline)
        if self.novel_orderby == 0:
            url_with_args += '&filter=author&orderby=' + str(orderby_dict.get(self.novel_orderby))
        else:
            url_with_args += '&filter=reply&orderby=' + str(orderby_dict.get(self.novel_orderby))
        return url_with_args

    def get_finished_novel(self):
        logging.info('===Get Novel Page===')
        url = self.get_url_with_args()
        novel_bs = load_web(url)

        all_page_count = get_all_page_count(novel_bs)

        for i in range(all_page_count):
            







