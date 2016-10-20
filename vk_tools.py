import vk
import requests
import time
import os


def handle_request(function):
    def new_function(*args, **kwargs):
        while True:
            try:
                return function(*args, **kwargs)
            except vk.exceptions.VkAPIError as e:
                # todo code review
                if e.is_captcha_needed is False:
                    raise
                sid = e.captcha_sid
                img = e.captcha_img
                print("Captcha img available at {}".format(img))
                time.sleep(120)
                key = new_function(requests.get(os.environ["captcha_solution_url"]).content)
                print("Captcha key is {}".format(key))
                while True:
                    try:
                        return function(*args, **kwargs, captcha_key=key, captcha_sid=sid)
                    except requests.exceptions.ReadTimeout:
                        pass

            except requests.exceptions.ReadTimeout:
                pass
    return new_function


@handle_request
def api_get_status(target, api):
    return api.users.get(user_ids=target, fields="status")


@handle_request
def api_get_name(target, api):
    return api.users.get(user_ids=target, fields="sex")


@handle_request
def api_send_message(target, message, api):
    return api.messages.send(user_id=target, message=message, v="4.104")


@handle_request
def api_get_last_messages(user_id, api):
    return api.messages.getHistory(user_id=user_id, offset=0, count=20, start_message_id=0, v="4.104")


async def get_name(target, queue, api):
    info = (await queue.enqueue(api_get_name, target, api))[0]
    first_name = info["first_name"]
    last_name = info["last_name"]
    name = first_name + " " + last_name
    gender = info["sex"] == 1
    return name, gender, first_name, last_name


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
    messages = [(message["mid"], message["from_id"], message["body"]) for message in result if type(message) != int]
    messages.reverse()
    return messages
