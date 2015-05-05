import requests

def send(key, link):
    response = requests.post('https://api.justyo.co/yoall/', {
        'api_token': key,
        'link': link
    })
    if "error" not in response:
        return True
    else:
        print("Error with sending YO")
        return False