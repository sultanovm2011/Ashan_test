import pickle5 as pickle
from urlextract import URLExtract
from urllib.parse import urlparse
import requests
from loguru import logger
# import threading
# import time
# import multiprocessing
import sys


outfile = open('messages_to_parse2.dat','rb')
d = pickle.load(outfile)
outfile.close()

extractor = URLExtract()
urls = extractor.find_urls(str(d))
dict1 = {}
dict2 = {}
dict3 = {}


def check_link(urls):
    for url in urls:
        try:
            link = urlparse(url)
            domen = link.netloc
            if not domen:
                logger.add("file_X.log", retention="20 minutes", rotation="5 minutes")
                logger.debug('Неизвестный URL:  ' + url)
                continue

            html = requests.head(url, timeout = 10)
            dict1[url] = html.status_code
            logger.info(url + '-----' + str(html.status_code))
            
            if html.status_code != 301:
                continue
            url_unshorten = html.headers['Location']
            url_unshorten = url_unshorten.replace('www.', '')

            if url != url_unshorten:
                dict2[url] = html.status_code
                dict3[url] = html.headers['Location']
                logger.info(url + '-----' + html.headers['Location'])
            # time.sleep(300)
        except Exception:
            inst = sys.exc_info()[1]
            logger.debug(inst.args[0])
            # time.sleep(300)
    print(dict1)
    print(dict2)
    print(dict3)

check_link(urls)
