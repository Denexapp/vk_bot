import vk_tools
import asyncio
import datetime
import time
import re


class ScheduleBot:
    def __init__(self, filename, dialogue, queue, api):
        self.dialogue = dialogue
        self.last_message_id = None
        self.schedule = Schedule(filename)
        self.api = api
        self.queue = queue

    def lesson_to_text(self, lesson):
        pass

    def decode_message(self, message):
        message = str(message).lower().strip()
        if not message.startswith("бот " or "бот," or "бот!" or "бот:"):
            return
        # todo разобраться с таймзонами
        date = datetime.datetime.now(datetime.tzinfo())
        message = message[4:]
        message = re.sub(r"\d", " ", message)
        words = [word for word in re.split("\W", message) if word != ""]
        if "сегодня" in words:
            pass
            # todo
        elif "завтра" in words:
            pass
            # todo
        else:
            # todo
            weekdays = self.schedule.get_weekdays()
            for x in range(len(weekdays)):
                if weekdays[x][:-1].lower() in words:
                    pass
                    # todo
                    break
        # todo
        return Question()

    def generate_answer(self, question, name):
        answer = name + ", "
        qtype = question.question_type
        qtime = question.time_type
        now = datetime.datetime.now(datetime.timezone(datetime.timedelta()))
        print("Schedule: datetime now is {}".format(now))
        if qtype == QuestionType.incorrect:
            answer += "я не понял запрос."
        elif qtype == 0:
            if qtime == TimeType.was:
                answer += "список преподавателей, учивших"
        return answer

    async def run(self):
        while True:
            messages = await vk_tools.get_last_messages(self.dialogue, self.queue, self.api)
            if self.last_message_id is None:
                self.last_message_id = messages[len(messages)-1][0]
            for mid, user, message in messages:
                if mid <= self.last_message_id:
                    continue
                else:
                    self.last_message_id = mid
                question = self.decode_message(message)
                if not question:
                    continue
                print("Schedule: question user is {}".format(user))
                name = await vk_tools.get_name(user, self.queue, self.api)
                print("Schedule: username is {}".format(name))
                answer = self.generate_answer(question, name)
                vk_tools.send_message(self.dialogue, answer, self.queue, self.api)
            await asyncio.sleep(10)


class Schedule:
    def __init__(self, filename):
        self.lessons_start_time = {}
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
                lesson_time = time.strptime(line[1], "%H:%M")
                self.lessons_start_time[key] = lesson_time

            week_day = ""
            lessons = None
            while True:
                line = file.readline()
                if line == "":
                    break
                line = line.strip()
                if line.startswith(">"):
                    week_day = line[1:].strip()
                    lessons = {}
                elif line.startswith("."):
                    self.schedule.append((week_day, lessons))
                else:
                    divider = line.find(" ")
                    key = line[0:divider]
                    lesson_time = None
                    if "@" in key:
                        key = key.split("@")
                        lesson_time = time.strptime(key[1], "%H:%M")
                        key = int(key[0])
                    else:
                        key = int(key)
                        lesson_time = self.lessons_start_time[key]
                    line = line[divider+1:].strip()
                    def parse_lesson(line):
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
                        return Lesson(name, lesson_time, key, rooms, teacher)
                    if "|" in line:
                        line = line.split("|")
                        lessons[key] = (parse_lesson(line[0]), parse_lesson(line[1]))
                    else:
                        lessons[key] = parse_lesson(line)

    def get_weekdays(self):
        return [day[0] for day in self.schedule]

class Lesson:
    def __init__(self, name, time, number, rooms=None, teacher=None):
        self.name = name
        self.time = time
        self.number = number
        self.rooms = [] if rooms is None else rooms
        self.teacher = teacher

class QuestionType:
    incorrect = -1
    teacher = 0
    where = 1
    amount = 2
    which = 3
    help = 4

class TimeType:
    was = -2
    previous = -1
    current = 0
    next = 1
    left = 2
    time = 4
    number = 5

class Question:
    def __init__(self):
        self.time_type = TimeType.current
        self.question_type = QuestionType.incorrect
        self.time = None
        self.day = None
        self.lesson_number = None