import json
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import requests
from config import LINKBASE
from parser import AdvertisementPageParser


class CrawlerBase(ABC):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def store(self, data):
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

    def start(self, url):
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

    def start_zommit(self):
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
        # self.parser = AdvertisementPageParser

    @staticmethod
    def __load_links():
        with open('storelist/data.json', 'r') as f:
            link = json.loads(f.read())
            return link

    def parse_links(self, html_data):
        soup = BeautifulSoup(html_data, 'html.parser')
        data = dict(title=None, price=None)
        title_tag = soup.find('h1',
                              attrs={'class': 'product_title entry-title'})
        if title_tag:
            data['title'] = title_tag.text
        price_tag = soup.find('span', attrs={'class':'woocommerce-Price-amount amount'})
        if price_tag:
            data['price'] = price_tag.text

        return data

    def start(self):
        for links in self.link:
            response = requests.get(links)
            data = self.parse_links(response.text)
            print(data)

    def store(self, data):
        with open('storelist/data.json', 'w') as f:
            f.write(json.dumps(data))

