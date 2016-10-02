import vk
import requests
import time
import os


def handle_captcha(function):
    def new_function(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except vk.exceptions.VkAPIError as e:
            sid = e.captcha_sid
            img = e.captcha_img
            print("Captcha img available at {}".format(img))
            time.sleep(60)
            key = requests.get(os.environ["captcha_solution_url"]).content
            print("Captcha key is {}".format(key))
            return function(*args, **kwargs, captcha_key=key, captcha_sid=sid)

    return new_function