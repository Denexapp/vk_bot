import threading


class VkBot:
    def __init__(self, api, queue):
        self.api = api
        self.queue = queue
        self.thread = threading.Thread(target=self.loop)

    def run(self):
        self.thread.start()

    def loop(self):
        pass
