import vk_tools
import curio
import vk_bot


class StatusChecker(vk_bot.VkBot):
    def __init__(self, queue, listener, target, api):
        super(StatusChecker, self).__init__(api, queue)
        self.listener = listener
        self.target = "id" + str(target)
        self.status = None
        self.name = None
        self.gender = None

    async def loop(self):
        print("StatusChecker: started.")
        target_info = await vk_tools.get_name(self.target, self.queue, self.api)
        self.name = target_info["name"]
        self.gender = target_info["gender"]
        print("StatusChecker: Received name {}".format(self.name))
        while True:
            status = await vk_tools.get_status(self.target, self.queue, self.api)
            if self.status is None:
                self.status = status
                message = "{} has status \"{}\"" \
                    .format(self.name, status)
                print("StatusChecker: " + message)
            elif status != self.status:
                self.status = status
                message = "{} has changed {} status to \"{}\""\
                    .format(self.name, "her" if self.gender else "his", status)
                print("StatusChecker: " + message)
                await vk_tools.send_message(self.listener, message, self.queue, self.api)
            await curio.sleep(10)
