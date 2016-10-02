import asyncio
import myqueue as queue_file
import status_checker as status_checker_file
import vk
import os


async def run():
    queue = queue_file.Queue()
    target = os.environ['target']
    listener = os.environ['listener']
    access_token = os.environ["access_token"]

    session = vk.Session(access_token=access_token)
    api = vk.API(session)

    status_checker = status_checker_file.StatusChecker(queue, listener, target, api)
    status_checker.run()
    while True:
        await asyncio.sleep(10)


loop = asyncio.get_event_loop()
loop.run_until_complete(run())
loop.close()
