import sys
import os


import numpy as np
from twocaptcha import TwoCaptcha
import requests
from bs4 import BeautifulSoup


sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
DOWNLOADED_CAPTCHA = []


def split_receivers(receivers, senders):
    count_for_sender = int(len(receivers) / len(senders))
    chunk_count = int(len(receivers) / count_for_sender)
    chunked_receivers = np.array_split(receivers, chunk_count)
    return {s: r.tolist() for s, r in zip(senders, chunked_receivers)}


def get_captcha_url(html):
    soup = BeautifulSoup(html, "html.parser")
    capcha_block = soup.find('div', {'class': 'ComposeReactCaptcha-ImageContainer'})
    images = capcha_block.find_all('img')
    for img in images:
        if img.has_attr('src'):
            img_url = img['src']
            return img_url
        else:
            print('captcha not found')


def download_captcha(img_url):
    filename = img_url.split("/")[-1]
    r = requests.get(img_url, timeout=0.5)
    if r.status_code == 200:
        with open(filename + '.jpg', 'wb') as f:
            f.write(r.content)
    DOWNLOADED_CAPTCHA.append(filename + '.jpg')
    return str(filename + '.jpg')


def captcha_response(img_name, captcha_api_key):
    print('посылаем капчу на разгаду')
    api_key = os.getenv('APIKEY_2CAPTCHA', f'{captcha_api_key}')
    solver = TwoCaptcha(api_key)
    result = solver.normal(f'{img_name}')
    return result['code']


def captcha_three(html, captcha_api_key):
    img_url = get_captcha_url(html)  # выдергиваем ссылку на изображение
    img_name = download_captcha(img_url)  # качам капчу
    catcha_code = captcha_response(img_name, captcha_api_key)
    #for delete_f in DOWNLOADED_CAPTCHA:
        #os.remove(delete_f)
    return catcha_code
