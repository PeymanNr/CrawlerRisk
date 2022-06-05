from bs4 import BeautifulSoup


class AdvertisementPageParser:

    def __init__(self):
        self.soup =None

    def parse_links(self, response_text):

        self.soup = BeautifulSoup(response_text, 'html.parser')
        data = dict(title=self.title, price=self.price)
        return data

    @property
    def title(self):
        title_tag = self.soup.find('h1', attrs={'class': 'product_title entry-title'})
        if title_tag:
            return title_tag.text

    @property
    def price(self):
        price_tag = self.soup.find('span', attrs={'class': 'woocommerce-Price-amount amount'})
        if price_tag:
            return price_tag.text


