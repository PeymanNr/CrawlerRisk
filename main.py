import store

from crawl import LinkCrawler, DataCrawler

if __name__ == '__main__':

    # result = LinkCrawler()
    # result.start_zommit(store=True)
    result = DataCrawler()
    result.start(store=True)