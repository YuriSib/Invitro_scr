import requests
from pprint import pprint

from app.parse.common_data import cookies, headers, params


class InvitroScrapper:
    @staticmethod
    def _fetch_data(url) -> requests.Response:
        return requests.get(
            url,
            params=params,
            cookies=cookies,
            headers=headers,
        )

    @staticmethod
    def _validation(response: requests.Response) -> str:
        if response.status_code != 200:
            return 'статус код != 200.'
        try:
            response.json()
        except Exception:
            return 'Не удается преобразовать полученные данные в словарь.'
        return "OK"

    def get_categories_tests(self) -> dict | str:
        """Сделает запрос к API Invitro и достанет список всех категорий анализов."""
        response = self._fetch_data('https://www.invitro.ru/golk/tests/api/v1/tests/categories')
        result = self._validation(response)
        if result != 'OK':
            return result

        categories = {}
        for category in response.json():
            for subcategory in category['subcategories']:
                categories[subcategory['id']] = subcategory['title']

        return categories

    def get_categories_complexes(self) -> dict | str:
        """Сделает запрос к API Invitro и достанет список всех категорий анализов."""
        try:
            response = self._fetch_data('https://www.invitro.ru/golk/tests/api/v1/complexes/categories')
            result = self._validation(response)
        except Exception as e:
            return str(e)
        if result != 'OK':
            return result

        categories = {}
        for category in response.json():
            categories[category['id']] = category['title']

        return categories

    def get_checkups(self) -> list[dict] | str:
        """Сделает запрос к API Invitro и достанет список всех категорий анализов."""
        try:
            response = self._fetch_data('https://www.invitro.ru/golk/tests/api/v1/checkups/')
            result = self._validation(response)
        except Exception as e:
            return str(e)
        if result != 'OK':
            return result

        services_clear_data = []
        for service in response.json()['data']:
            title = service['title']
            price = service['price']

            services_clear_data.append({"title": title, "price": price})

        return services_clear_data

    def get_services(self, category_id: str, category_type="tests") -> list[dict] | str:
        """сделает запрос к API Invitro и достанет список всех услуг по данному ID категории"""
        url = f'https://www.invitro.ru/golk/tests/api/v1/{category_type}/categories/{category_id}'
        response = self._fetch_data(url)
        result = self._validation(response)
        if result != 'OK':
            return result

        services_data = response.json().get('data')
        if not services_data:
            return "JSON был извлечен, но необходимых данных в нем нет."

        services_clear_data = []
        for service in services_data:
            title = service['title']
            price = service['price']

            services_clear_data.append({"title": title, "price": price})

        return services_clear_data


if __name__ == '__main__':
    # scraper = InvitroScrapper()
    # categories = scraper.get_services("4fad3634-4bf2-414d-84fb-5c3fa429e148")
    # print(len(categories))

    response = requests.get(
        'https://www.invitro.ru/golk/tests/api/v1/tests/categories',
        params=params, cookies=cookies, headers=headers)
    data = response.json()
    pass


    # response = requests.get(
    #     f'https://www.invitro.ru/golk/tests/api/v1/{'tests'}/categories/{'3670df48-3e4a-4441-b05f-07b2124d7ef2'}', params=PARAMS_C, cookies=COOKIES_C, headers=HEADERS_C)
    # data = response.json()
    # print(pprint(data, indent=4, width=40))