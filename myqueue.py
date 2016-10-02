import time
import threading
import asyncio


class Queue:
    def __init__(self):
        self.queue = []
        self.queue_current = 1
        self.queue_last_item = 0
        self.queue_upper_limit = 200
        self.queue_lock = threading.Lock()
        self.interval = 1
        self.last_request_time = time.time() - self.interval

    def increment(self, value):
        value += 1
        if value < self.queue_upper_limit:
            return value
        else:
            return 0

    async def enqueue(self, function, *args, **kwargs):
        self.queue_lock.acquire()
        self.queue_last_item = self.increment(self.queue_last_item)
        queue_number = self.queue_last_item
        self.queue_lock.release()
        while not queue_number == self.queue_current:
            await asyncio.sleep(0.2)
        sleep_time = self.last_request_time - time.time() + 1
        await asyncio.sleep(sleep_time if sleep_time >= 0 else 0)
        print("Type of 'function' is {}".format(type(function)))
        result = await function(*args, **kwargs)
        self.queue_current = self.increment(self.queue_current)
        return result

