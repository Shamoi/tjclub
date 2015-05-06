import requests
import json
import time
import re
from send_yo import send
from config import ACCESS_KEY, COMMUNITY_ID

# Регулярное выражения для поиска URL
url_regexp = re.compile(r'[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)',
                        re.IGNORECASE)
vk_api_url = 'https://api.vk.com/method/wall.get?owner_id={owner_id}&count={count}'.format(
    owner_id=str(COMMUNITY_ID),
    count=1
)
response = json.loads(requests.get(vk_api_url).text)

# Если есть закрепленная запись, то мы в дальнейшем берем сразу
# две записи и работаем со второй. Иначе - берем одну и
# работаем с ней.
if 'is_pinned' in response['response'][1]:
    n = 2
else:
    n = 1

vk_api_url = 'https://api.vk.com/method/wall.get?owner_id={owner_id}&count={count}'.format(
    owner_id=str(COMMUNITY_ID),
    count=n
)
try:
    last_post_id = int(open('last_post_id.txt').read())
except FileNotFoundError:
    last_post_id = response['response'][n]['id']


while True:
    response = json.loads(requests.get(vk_api_url).text)
    try:
        new_post_id = response['response'][n]['id']
    except IndexError:
        time.sleep(5)
        continue
    if new_post_id != last_post_id:
        last_post_id = new_post_id

        # Ищем URL в нужном посте и отправляем его
        # как ссылку в Yo
        post_link = re.search(url_regexp, response['response'][n]['text'])
        if post_link is not None:
            send_url = post_link.string[post_link.start():post_link.end()]
            send(key=ACCESS_KEY,
                 link=send_url)

    open('last_post_id.txt', 'w').write(str(last_post_id))
    time.sleep(5)