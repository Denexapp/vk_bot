import os
import time
import vk
import myqueue as queue_file
import status_checker as status_checker_file
import schedule as schedule_file


if __name__ == '__main__':
    queue = queue_file.Queue()
    target = os.environ["status_target"]
    listener = os.environ["status_listener"]
    access_token = os.environ["access_token"]
    schedule_filename = os.environ["schedule_filename"]
    schedule_dialogue = os.environ["schedule_dialogue"]
    # the app also uses environment variable "captcha_solution_url" in module vk_tools

    session = vk.Session(access_token=access_token)
    api = vk.API(session)

    status_checker = status_checker_file.StatusChecker(queue, listener, target, api)
    schedule = schedule_file.ScheduleBot(schedule_filename, schedule_dialogue, queue, api)

    status_checker.run()
    schedule.run()

    while True:
        time.sleep(100)
