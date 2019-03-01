import requests, time, random, re, codecs, os, errno;
from bs4 import BeautifulSoup as bs;

BASE_URL = 'https://ck101.com/forum.php?mod=forumdisplay&fid=3419'

type_dict = {0: '', 1: '2399', 2: '2400', 3: '2401', 4: '2402', 5: '2403', 6: '2404', 7: '2405'}
dateline_dict = {0: '', 1: '86400', 2: '172800', 3: '604800', 4: '2592000', 5: '7948800'}
orderby_dict = {0: 'dateline', 1: 'replies', 2: 'views'}


def load_web(url):
    print('===Load Web: {0} ==='.format(url))

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4'
    }
    web_res = requests.get(url, headers=headers)
    web_res.encoding = 'utf8'
    time.sleep(random.uniform(0, 2))
    web_bs = bs(web_res.text, 'lxml')
    return web_bs


# Get All Novel Page Count
def get_all_page_count(web_bs):
    fd_page_bottom = web_bs.find('span', id='fd_page_bottom')
    if fd_page_bottom.text == '':
        return 1
    else:
        last_tag = fd_page_bottom.select_one('div').find('a', attrs={'class': 'last'}).text
        return int(last_tag.split(' ')[1])


# Get a Novel Page Count
def get_novel_page_count(novel_bs):
    pgt = novel_bs.find('div', id='pgt')
    pg_class = pgt.find('div', class_='pgt').find('div', class_='pg')
    last_tag = pg_class.find('a', attrs={'class': 'last'})
    if last_tag:
        return int(last_tag.text.split(' ')[1])
    else:
        return int(pgt.find('div', class_='pgt').find('div', class_='pg').find_all('a')[-2].text)


def get_novel_title(novel_bs):
    return novel_bs.find('h1', id='thread_subject').text


def create_dir(filepath):
    if not os.path.exists(os.path.dirname(filepath)):
        try:
            os.makedirs(os.path.dirname(filepath))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise


def store_file(filename, data, mode):
    create_dir(filename)
    with codecs.open(filename, mode, encoding='utf-8') as f:
        f.write(data)


def read_file(filename, mode='r'):
    with codecs.open(filename, mode, encoding='utf-8') as f:
        return f.read()


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

    def get_novel(self, url):
        novel_bs = load_web(url)
        novel_page_count = get_novel_page_count(novel_bs)
        novel_title = get_novel_title(novel_bs)
        novel_path = os.path.join(self.file_dir, novel_title + '.txt')
        print('Novel Title:', novel_title)
        print('Page Count:', novel_page_count)

        store_file(filename=novel_path, data=novel_title, mode='w+')
        for i in range(novel_page_count):
            novel_info_bs = load_web(url + '&page=' + str(i + 1))

            for novel_post in novel_info_bs.find_all('td', id=re.compile('^postmessage_')):
                store_file(filename=novel_path, data='\n' + novel_post.text, mode='a')

    def get_finished_novel(self):
        print('===Get Novel Page===')
        url = self.get_url_with_args()
        all_page_bs = load_web(url)

        all_page_count = get_all_page_count(all_page_bs)
        novel_link_list = []

        # Get All Novel Link
        for i in range(all_page_count):
            novel_bs = load_web(url + '&page=' + str(i + 1))
            novel_page_bs = novel_bs.find('table', id='threadlisttableid').findAll('tbody', id=re.compile('^normalthread_'))

            for novel in novel_page_bs:
                novel_link_list.append(novel.find('div', class_='blockTitle').find('a', class_='s xst')['href'])

        for novel_link in novel_link_list:
            self.get_novel(novel_link)







