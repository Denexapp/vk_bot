import myqueue as queue_file
import status_checker as status_checker_file
import vk
import os
import time


async def run():
    queue = queue_file.Queue()
    target = os.environ['target']
    listener = os.environ['listener']
    access_token = os.environ["access_token"]

    session = vk.Session(access_token=access_token)
    api = vk.API(session)

    status_checker = status_checker_file.StatusChecker(queue, listener, target, api)
    await status_checker.run()

run()
while True:
    time.sleep(10)
