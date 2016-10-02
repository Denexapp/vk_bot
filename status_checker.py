import vk_tools
import requests
import time


class StatusChecker:
    def __init__(self, queue, listener, target, api):
        self.queue = queue
        self.listener = listener
        self.target = "id" + str(target)
        self.api = api
        self.status = None
        self.name = None
        self.gender = None

    @vk_tools.handle_captcha
    def api_get_status(self, target):
        return self.api.users.get(user_ids=target, fields="status")

    @vk_tools.handle_captcha
    def api_get_name(self, target):
        return self.api.users.get(user_ids=target, fields="sex")

    @vk_tools.handle_captcha
    def api_send_message(self, target, message):
        return self.api.messages.send(user_id=target, message=message, v="4.104")

    async def get_name(self, target):
        target_info = await self.queue.enqueue(self.api_get_name, target)[0]
        target_name = target_info["first_name"] + " " + target_info["last_name"]
        target_gender = target_info["sex"] == 1
        return target_name, target_gender

    async def get_status(self, target):
        while True:
            try:
                return await self.queue.enqueue(self.api_get_status, target)[0]["status"]
            except requests.exceptions.ReadTimeout:
                pass

    async def send_message(self, target, message):
        await self.queue.enqueue(self.api_send_message, target, message)

    async def run(self):
        self.name, self.gender = await self.get_name(self.target)
        while True:
            status = await self.get_status(self.target)
            if status is None:
                self.status = status
            elif status != self.status:
                self.status = status
                await self.send_message(self.listener, "{} has changed {} status to \"{}\""
                                        .format(self.name, "her" if self.gender else "his", status))
            time.sleep(10)
