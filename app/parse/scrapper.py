import requests

from app.parse.common_data import PARAMS, HEADERS, COOKIES


response = requests.get(
    'https://www.invitro.ru/golk/tests/api/v1/complexes/categories/749c4082-aba7-40ca-8fde-8481f8212c5a',
    params=PARAMS,
    cookies=COOKIES,
    headers=HEADERS,
).json()
data = response['data']
pass