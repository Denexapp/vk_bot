import vk
import requests
import time
import os


def handle_captcha(function):
    def new_function(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except vk.exceptions.VkAPIError as e:
            # todo handle only captcha
            sid = e.captcha_sid
            img = e.captcha_img
            print("Captcha img available at {}".format(img))
            time.sleep(60)
            key = requests.get(os.environ["captcha_solution_url"]).content
            print("Captcha key is {}".format(key))
            return function(*args, **kwargs, captcha_key=key, captcha_sid=sid)

    return new_function


@handle_captcha
def api_get_status(target, api):
    return api.users.get(user_ids=target, fields="status")


@handle_captcha
def api_get_name(target, api):
    return api.users.get(user_ids=target, fields="sex")


@handle_captcha
def api_send_message(target, message, api):
    return api.messages.send(user_id=target, message=message, v="4.104")


@handle_captcha
def api_get_last_messages(user_id, api):
    return api.messages.getHistory(user_id=user_id, offset=0, count=20, start_message_id=0, v="4.104")


async def get_name(target, queue, api):
    target_info = (await queue.enqueue(api_get_name, target, api))[0]
    target_name = target_info["first_name"] + " " + target_info["last_name"]
    target_gender = target_info["sex"] == 1
    return target_name, target_gender


async def get_status(target, queue, api):
    while True:
        try:
            return (await queue.enqueue(api_get_status, target, api))[0]["status"]
        except requests.exceptions.ReadTimeout:
            pass


async def send_message(target, message, queue, api):
    await queue.enqueue(api_send_message, target, message, api)


async def get_last_messages(user_id, queue, api):
    result = await queue.enqueue(api_get_last_messages, user_id, api)
    print(result)
    messages = [(message["mid"], message["from_id"], message["body"]) for message in result if "body" in message]
    messages.reverse()
    return messages
