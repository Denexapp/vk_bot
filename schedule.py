import vk_tools
import asyncio
import datetime
import time


class ScheduleBot:
    def __init__(self, filename, dialogue, queue, api):
        self.dialogue = dialogue
        self.last_message_id = None
        self.schedule = Schedule(filename)
        self.api = api
        self.queue = queue

    async def run(self):
        while True:
            messages = await vk_tools.get_last_messages(self.dialogue, self.queue, self.api)
            await asyncio.sleep(10)


class Schedule:
    def __init__(self, filename):
        self.lesions_start_time = {}
        self.duration = 0
        self.schedule = []

        with open(filename) as file:
            self.duration = int(file.readline().strip())
            while True:
                line = file.readline().strip()
                if line.startswith("."):
                    break
                line = line.split(" ")
                key = int(line[0])
                lesion_time = time.strptime(line[1], "%H:%M")
                self.lesions_start_time[key] = lesion_time

            week_day = ""
            lesions = None
            while True:
                line = file.readline()
                if line == "":
                    break
                line = line.strip()
                if line.startswith(">"):
                    week_day = line[1:].strip()
                    lesions = {}
                elif line.startswith("."):
                    self.schedule.append((week_day, lesions))
                else:
                    divider = line.find(" ")
                    key = line[0:divider]
                    lesion_time = None
                    if "@" in key:
                        key = key.split("@")
                        lesion_time = time.strptime(key[1], "%H:%M")
                        key = int(key[0])
                    else:
                        key = int(key)
                        lesion_time = self.lesions_start_time[key]
                    line = line[divider+1:].strip()
                    def parse_lesion(line):
                        if line.strip() == "":
                            return None
                        items = [x.strip() for x in line.split(";")]
                        name = items[0]
                        rooms = []
                        teacher = None
                        if len(items) >= 2:
                            rooms = [x.strip for x in items[1].split(',')]
                        if len(items) >= 3:
                            teacher = items[2]
                        return Lesion(name, lesion_time, rooms, teacher)
                    if "|" in line:
                        line = line.split("|")
                        lesions[key] = (parse_lesion(line[0]), parse_lesion(line[1]))
                    else:
                        lesions[key] = parse_lesion(line)


class Lesion:
    def __init__(self, name, time, rooms=None, teacher=None):
        self.name = name
        self.time = time
        self.rooms = [] if rooms is None else rooms
        self.teacher = teacher
