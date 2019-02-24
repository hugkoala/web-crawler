# Execute with
# $ python ck101_web_crawler/__main__.py

import ck101_web_crawler

if __name__ == '__main__':
    # ck101_web_crawler.main()
    ck101_web_crawler = ck101_web_crawler.CK101WebCrawler(novel_type=1, novel_dateline=3,
                                            novel_orderby=1, file_dir='.')
    ck101_web_crawler.get_url_with_args()



