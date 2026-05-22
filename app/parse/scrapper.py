import requests

from app.parse.common_data import PARAMS, HEADERS, COOKIES


class InvitroScrapper:
    def __init__(self):
        self.params = PARAMS
        self.headers = HEADERS
        self.cookies = COOKIES

    @staticmethod
    def _fetch_data(url) -> requests.Response:
        return requests.get(
            url,
            params=PARAMS,
            cookies=COOKIES,
            headers=HEADERS,
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
                categories[subcategory['title']] = subcategory['id']

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
            categories[category['title']] = category['id']

        return categories

    def get_checkups(self):
        """Сделает запрос к API Invitro и достанет список всех категорий анализов."""
        try:
            response = self._fetch_data('https://www.invitro.ru/golk/tests/api/v1/checkups/')
            result = self._validation(response)
        except Exception as e:
            return str(e)
        if result != 'OK':
            return result

        categories = {}
        for category in response.json():
            categories[category['title']] = category['id']

        return categories

    def get_services(self, category_id: str, category_type="tests") -> list[dict] | str:
        """сделает запрос к API Invitro и достанет список всех услуг по данному ID категории"""
        response = self._fetch_data(f'https://www.invitro.ru/golk/tests/api/v1/{category_type}/categories/{category_id}')
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
    scraper = InvitroScrapper()
    categories = scraper.get_checkups()
    print(len(categories))