from bs4 import BeautifulSoup


class AdvertisementPageParser:

    def __init__(self):
        self.soup = None

    def parse_links(self, response_text):

        self.soup = BeautifulSoup(response_text, 'html.parser')
        data = dict(title=self.title, price=self.price,
                    product_id=self.product_id)
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

    @property
    def product_id(self):
        id_tag = self.soup.select_one('#tab-description > p')
        if id_tag:
            return id_tag.text.replace('بارکد محصول(barcode)', '')

    # @property
    # def image_id(self):
    #     image_id = self.soup.select_one('#product-43553 > div.product-main.clearfix > div.gallery-container > div > figure > div')
    #     if image_id:
    #         return image_id
    #

