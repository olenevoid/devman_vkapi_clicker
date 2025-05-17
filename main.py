import requests
from dotenv import load_dotenv
from os import environ
from urllib.parse import urlparse


VK_API_VERSION = '5.199'


def shorten_link(token: str, url: str, private: int = 0) -> str:
    params = {
        'access_token': token,
        'v': VK_API_VERSION,
        'url': url,
        'private': private
        }

    request_url = 'https://api.vk.ru/method/utils.getShortLink'

    response = requests.get(request_url, params=params)

    response.raise_for_status()

    response_data = response.json()

    if 'error' in response_data:
        raise requests.exceptions.InvalidURL(response=response)

    short_link = response_data['response']['short_url']

    return short_link


def count_clicks(token: str, url: str) -> int | None:
    parsed_link = urlparse(url)
    params = {
        'access_token': token,
        'v': VK_API_VERSION,
        'key': parsed_link.path.replace('/', ''),
        'interval': 'forever',
        'extended': 0
        }

    request_url = 'https://api.vk.ru/method/utils.getLinkStats'

    response = requests.get(request_url, params=params)

    response.raise_for_status()

    response_data = response.json()

    if 'error' in response_data:
        raise requests.exceptions.InvalidURL(response=response)

    stats = response_data['response']['stats']

    if len(stats) < 1:
        return None

    views = stats[0]['views']

    return views


def is_vkcc_link(url) -> bool:
    parsed_link = urlparse(url)

    if parsed_link.hostname != 'vk.cc':
        return False

    return True


def main():
    load_dotenv()
    vk_token = environ['VK_TOKEN']

    url = input('Введите ссылку: ')
    try:
        if is_vkcc_link(vk_token, url):

            clicks = count_clicks(vk_token, url)

            if clicks is None:
                print('Возможно, превышен лимит обращений к API.')
            else:
                print('Количество кликов:', clicks)

        else:

            short_link = shorten_link(vk_token, url)
            print('Сокращенная ссылка:', short_link)

    except requests.exceptions.InvalidURL:
        print('Вы ввели неверную ссылку')


if __name__ == '__main__':
    main()
