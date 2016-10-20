import threading
import time


class VkBot:
    def __init__(self, api, queue):
        self.api = api
        self.queue = queue

    def run(self):
        def restart_loop():
            try:
                threading.Thread(target=self.loop)
            except Exception as e:
                print(e)
                print("Thread throw an exception, restart in 10 seconds")
                time.sleep(10)
        threading.Thread(target=restart_loop).start()

    def loop(self):
        pass
