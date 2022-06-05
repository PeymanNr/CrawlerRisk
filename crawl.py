import json
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import requests
from config import LINKBASE
from parser import AdvertisementPageParser


class CrawlerBase(ABC):
    @abstractmethod
    def start(self, store):
        pass

    @abstractmethod
    def store(self, data, filename=None):
        pass

    def get(self, link):
        try:
            response = requests.get(link)
        except:
            return None
        # print(response.status_code, response.url)
        return response


class LinkCrawler(CrawlerBase):

    def __init__(self, link=LINKBASE):
        self.link = link

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
            # print(f'page:', len(ad_link))

        return ad_link

    def start_zommit(self, store=False):
        result_list = list()
        links = self.start(self.link)
        for li in links:
            result_li = li.get('href')
            print(result_li)
            result_list.append(result_li)
        self.store(result_list)

    def store(self, data):
        with open('storelist/data.json', 'w') as f:
            f.write(json.dumps(data))


class DataCrawler(CrawlerBase):

    def __init__(self):
        self.link = self.__load_links()
        self.parser = AdvertisementPageParser()

    @staticmethod
    def __load_links():
        with open('storelist/data.json', 'r') as f:
            link = json.loads(f.read())
            return link

    def start(self, store=False):
        for links in self.link:
            response = requests.get(links)
            data = self.parser.parse_links(response.text)
            if store:
                self.store(data, data.get('title', 'sample'))

    def store(self, data, filename):
        with open(f'storelist/adv/{filename}.json', 'w') as f:
            f.write(json.dumps(data))
        print(f'storelist/adv/{filename}.json')
