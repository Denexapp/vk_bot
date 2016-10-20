import curio


class VkBot:
    def __init__(self, api, queue):
        self.api = api
        self.queue = queue

    async def run(self):
        try:
            print("DECORATOR")
            await self.loop()
        except curio.TaskError:
            raise Exception

    async def loop(self):
        pass
