from bs4 import BeautifulSoup


class AdvertisementPageParser:

    def parse_links(self):

        soup = BeautifulSoup('html.parser')
        # data = dict(title=None)
        title_tag = soup.find('h1', attrs={'class': 'product_title entry-title'})
        # data_links = title_tag.text
        # if title_tag:
        #     data['title'] = title_tag

        return title_tag
