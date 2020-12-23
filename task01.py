import json
import requests
import time


class ParserCatalog:
    _headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }

    def __init__(self, product_url, category_url):
        self.product_url = product_url
        self.category_url = category_url

    @staticmethod
    def _get(*args, **kwargs):
        while True:
            try:
                response = requests.get(*args, **kwargs)
                if response.status_code != 200:
                    raise Exception  # todo сделать класс ошибки для работы со статусами
                time.sleep(0.1)
                return response
            # todo Обработать конкретные ошибки
            except Exception:
                time.sleep(0.250)

    def get_categories(self, url):
        response = requests.get(url, headers=self._headers)
        response.encoding = "utf-8"
        print(response.text)
        return response.json()

    def get_products(self, category_code):
        params = {
            'records_per_page': 50,
            'categories': category_code
        }
        url = self.product_url
        while url:
            response = self._get(url, params=params, headers=self._headers)
            if params:
                params = {}
            response.encoding = "utf-8"
            data: dict = response.json()
            url = data.get('next')

            yield data.get('results')

    def run(self):
        for category in self.get_categories(self.category_url):
            data = {
                "name": category['parent_group_name'],
                'code': category['parent_group_code'],
                "products": [],
            }

            for products in self.get_products(category['parent_group_code']):
                data["products"].extend(products)
            self.save_to_json_file(
                data,
                category['parent_group_code']
            )

    @staticmethod
    def save_to_json_file(data: dict, file_name):
        with open(f'products/{file_name}.json', 'w', encoding='UTF-8') as file:
            json.dump(data, file, ensure_ascii=False)


if __name__ == '__main__':
    parser = ParserCatalog('https://5ka.ru/api/v2/special_offers/', 'https://5ka.ru/api/v2/categories/')
    parser.run()