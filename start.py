import requests
import json
import time
from send_yo import send
from config import ACCESS_KEY, COMMUNITY_ID

vk_api_url = 'https://api.vk.com/method/wall.get?owner_id={owner_id}&count=1'.format(
    owner_id=str(COMMUNITY_ID)
)

try:
    last_post_id = int(open('last_post_id.txt').read())
except FileNotFoundError:
    response = json.loads(requests.get(vk_api_url).text)
    last_post_id = response['response'][1]['id']


while True:
    response = json.loads(requests.get(vk_api_url).text)
    new_post_id = response['response'][1]['id']
    if new_post_id != last_post_id:
        last_post_id = new_post_id

        # Ищем последнюю строчку в посте, которая является
        # ссылкой на полный материал (в "новости часа").
        # Если этой ссылки нет, игнорируем запись.
        try:
            post_link = response['response'][1]['text'].split('<br>')[-1]
        except KeyError:
            continue

        send(key=ACCESS_KEY, link=post_link)

    open('last_post_id.txt', 'w').write(str(last_post_id))
    time.sleep(5)