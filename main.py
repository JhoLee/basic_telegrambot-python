# Test code for "Jho_RIPBot" echoing

import json
import time
import urllib

import requests

TOKEN = ""
# [START read_secrets]
with open('secrets.json') as secret_json:
    secret_data = json.load(secret_json)
    TOKEN = secret_data['TOKEN']
# [END read_secrets]

URL = "https://api.telegram.org/bot{token}/".format(token=TOKEN)


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    data = json.loads(content)
    return data


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={offset}".format(offset=offset)
    data = get_json_from_url(url)
    return data


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id):
    url = URL + "sendMessage?text={text}&chat_id={chat_id}" \
        .format(text=text, chat_id=chat_id)
    get_url(url)


def get_last_update_id(updates):
    """
    Calculates the highest ID of all the updates it receive from getUpdates.
    :param updates: getUpdates()
    :return: last update id
    """
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def echo_all(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            send_message(text, chat)
        except Exception as e:
            print(e)


def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={text}&chat_id={chat_id}" \
        .format(text=text, chat_id=chat_id)
    get_url(url)


def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        time.sleep(0.5)


if __name__ == "__main__":
    main()
