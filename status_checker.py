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
        print("StatusChecker: started.")
        self.name, self.gender = await vk_tools.get_name(self.target, self.queue, self.api)
        print("StatusChecker: Received name {}".format(self.name))
        while True:
            status = await vk_tools.get_status(self.target, self.queue, self.api)
            if self.status is None:
                self.status = status
            elif status != self.status:
                self.status = status
                message = "{} has changed {} status to \"{}\""\
                    .format(self.name, "her" if self.gender else "his", status)
                print("StatusChecker: " + message)
                await vk_tools.send_message(self.listener, message, self.queue, self.api)
            else:
                print("StatusChecker: {} still has status {}".format(self.name, status))
            await asyncio.sleep(10)
