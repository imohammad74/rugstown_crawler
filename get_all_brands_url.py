from datetime import datetime

import requests
from bs4 import BeautifulSoup
from db import DBManagement as db
from common import Common

now = datetime.now()


class GetAllBrandsURL:

    @staticmethod
    def main(params):
        """This function is main function in this script and get urls and insert them to database."""
        brand = params['brand']
        main_url = params['url']
        number_of_product = Common.number_of_product(params['soup'])
        url_list = Common.last_url(number_of_product)
        for url in url_list:
            if url == 0:
                plp_url = main_url
            else:
                plp_url = f"{main_url}&page={url}"
            r = requests.get(plp_url)
            soup = BeautifulSoup(r.content, "html.parser")
            a_tags = soup.find_all(class_='product-img has-second-image')
            for pdp_url in a_tags:
                current_time = int(now.strftime("%y%m%d"))
                ss = BeautifulSoup(str(pdp_url), "html.parser")
                el = ss.find(class_='product-img has-second-image', href=True)
                clean_url = el['href']
                db.insert_rows(db_file=db.db_file(), table_name=db.db_table()[0], log=False, unique_row=True, columns=[
                    {
                        'column': 'url_address',
                        'value': clean_url,
                    },
                    {
                        'column': 'last_update',
                        'value': current_time,
                    },
                    {
                        'column': 'brand',
                        'value': brand,
                    }
                ])
            print(f'{url} finish!')

    def __init__(self, params):
        self.main(params)
