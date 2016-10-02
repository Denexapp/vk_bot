import time
import threading
import asyncio


class Queue:
    def __init__(self):
        self.queue = []
        self.queue_current = 0
        self.queue_last_item = 0
        self.queue_upper_limit = 200
        self.queue_lock = threading.Lock()
        self.interval = 1
        self.last_request_time = time.time() - self.interval

    async def enqueue(self, function, *args, **kwargs):
        self.queue_lock.acquire()
        if self.queue_last_item < self.queue_upper_limit:
            self.queue_last_item += 1
        else:
            self.queue_last_item = 0
        queue_number = self.queue_last_item
        self.queue_lock.release()
        while not queue_number == self.queue_current:
            await asyncio.sleep(0.2)
        await time.sleep(self.last_request_time - time.time() + 1)
        result = await function(*args, **kwargs)
        self.queue_current += 1
        return result

