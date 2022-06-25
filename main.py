import sys

from crawl import LinkCrawler, DataCrawler, ImageDownloader

if __name__ == '__main__':
    switch = sys.argv[1]
    if switch == 'find_links':
        result = LinkCrawler()
        result.start_zommit(store=True)
    elif switch == 'extract_pages':
        result = DataCrawler()
        result.start(store=True)
    elif switch == 'download_image':
        crawler = ImageDownloader()
        crawler.start(store=True)