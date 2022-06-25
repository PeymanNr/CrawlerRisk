from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import requests

import login
from config import LINKBASE, STORAGE_TYPE
from parser import AdvertisementPageParser
from storage import MongoStorage, FileStorage
from login import get_cookie


class CrawlerBase(ABC):

    def __init__(self):
        self.storage = self.__set_storage()
        self.cookie = get_cookie()

    @staticmethod
    def __set_storage():
        if STORAGE_TYPE == 'file':
            return FileStorage()
        return MongoStorage()

    @abstractmethod
    def start(self, store):
        pass

    @abstractmethod
    def store(self, data, filename=None):
        pass

    def get(self, link):
        try:
            response = requests.get(link, cookies=self.cookie)
        except:
            return None
        return response


class LinkCrawler(CrawlerBase):

    def __init__(self, link=LINKBASE):
        self.link = link
        super().__init__()

    def find_links(self, html_doc):
        soup = BeautifulSoup(html_doc, 'html.parser')
        adv_list = soup.find_all('a',
                                 attrs={
                                     'class': 'woocommerce-LoopProduct-link woocommerce-loop-product__link'})
        return adv_list

    def start(self, url, store=False):
        start = 1
        crawl = True
        ad_link = list()
        while crawl:
            result_response = self.get(url.format(start))
            new_find = self.find_links(result_response.text)
            ad_link.extend(new_find)
            if start == 3:
                crawl = False
            start += 1

        return ad_link

    def start_zommit(self, store=False):
        adv_links = list()
        links = self.start(self.link)
        adv_links.extend(links)
        if store:
            self.store([{"url": li.get('href'), 'flag': False} for li in adv_links])

    def store(self, data, *args):
        self.storage.store(data, 'advertisements_links')


class DataCrawler(CrawlerBase):
    def __init__(self):
        super().__init__()
        self.links = self.__load_links()
        self.parser = AdvertisementPageParser()

    def __load_links(self):
        return self.storage.load()
    ###('advertisements_links', {'flag': False}
    def start(self, store=False):
        for li in self.links:
            response = requests.get(li['url'])
            data = self.parser.parse_links(response.text)
            if store:
                self.store(data, data.get('product_id', 'sample'))
            # self.storage.update_flag(li)

    def store(self, data, filename):
        self.storage.store(data, 'advertisement_data')
        print(data['product_id'])


class ImageDownloader(CrawlerBase):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.advertisement = self.__load_advertisements()

    def __load_advertisements(self):
        return self.storage.load('advertisement_data')

    def start(self, store=False):
        for advertisement in self.advertisement:
            for image in advertisement['image']:
                pass

    def store(self, data, filename):
        pass