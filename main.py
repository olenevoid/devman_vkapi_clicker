import requests
from dotenv import load_dotenv
from os import getenv
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

    try:
        response = make_request(params, request_url)
    except requests.exceptions.HTTPError:
        raise

    short_link = response.json()['response']['short_url']

    return short_link


def count_clicks(token: str, url: str) -> int | None:
    params = {
        'access_token': token,
        'v': VK_API_VERSION,
        'key': url.split('/')[-1],
        'interval': 'forever',
        'extended': 0
        }

    request_url = 'https://api.vk.ru/method/utils.getLinkStats'

    try:
        response = make_request(params, request_url)
    except requests.exceptions.HTTPError:
        raise

    stats = response.json()['response']['stats']

    if len(stats) < 1:
        return None

    views = stats[0]['views']

    return views


def is_shorten_link(url) -> bool:
    parsed = urlparse(url)
    if parsed.hostname == 'vk.cc':
        return True
    return False


def main():
    load_dotenv()
    vk_token = getenv('VK_TOKEN')

    url = input('Введите ссылку: ')
    try:
        if is_shorten_link(url):

            clicks = count_clicks(vk_token, url)
            if clicks:
                print('Количество кликов:', clicks)
            else:
                print('Возможно, превышен лимит обращений к API.')

        else:

            short_link = shorten_link(vk_token, url)
            print('Сокращенная ссылка:', short_link)

    except requests.exceptions.HTTPError:
        print('Неверная ссылка')


if __name__ == '__main__':
    main()
