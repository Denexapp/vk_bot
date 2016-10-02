import vk_tools
import asyncio


class StatusChecker:
    def __init__(self, queue, listener, target, api):
        self.queue = queue
        self.listener = listener
        self.target = "id" + str(target)
        self.api = api
        self.status = None
        self.name = None
        self.gender = None

    async def run(self):
        self.name, self.gender = await vk_tools.get_name(self.target, self.queue, self.api)
        print("StatusChecker: Received name {}".format(self.name))
        while True:
            status = await vk_tools.get_status(self.target, self.queue, self.api)
            print("StatusChecker: Got status {}".format(status))
            if status is None:
                self.status = status
            elif status != self.status:
                self.status = status
                await vk_tools.send_message(self.listener, "{} has changed {} status to \"{}\""
                                            .format(self.name, "her" if self.gender else "his", status),
                                            self.queue, self.api)
            await asyncio.sleep(10)
