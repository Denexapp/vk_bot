import vk_tools
import time
import vk_bot
import re


class ScheduleBot(vk_bot.VkBot):
    def __init__(self, filename, dialogue, queue, api):
        super(ScheduleBot, self).__init__(api, queue)
        self.dialogue = dialogue
        self.last_message_id = None
        self.schedule = Schedule(filename)

    def lesson_to_text(self, lesson):
        #todo
        pass

    def generate_answer(self, question, name):
        answer = name[0] + ", "
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

    def loop(self):
        print("Schedule: started.")
        while True:
            messages = vk_tools.get_last_messages(self.dialogue, self.queue, self.api)
            if self.last_message_id is None:
                self.last_message_id = messages[len(messages)-1][2]
            for mid, user, message in messages:
                if mid <= self.last_message_id:
                    continue
                else:
                    self.last_message_id = mid
                question = self.decode_message(message)
                if not question:
                    continue
                print("Schedule: question user is {}".format(user))
                name = vk_tools.get_name(user, self.queue, self.api)["name"]
                print("Schedule: username is {}".format(name))
                answer = self.generate_answer(question, name)
                vk_tools.send_message(self.dialogue, answer, self.queue, self.api)
            time.sleep(10)


class Schedule:
    def __init__(self, filename):
        self.lessons_start_time = {}
        self.duration = 0
        self.schedule = []
        self.timezone = 0

        with open(filename) as file:
            self.timezone = int(file.readline().split(":")[1].strip())
            self.duration = int(file.readline().split(":")[1].strip())
            while True:
                line = file.readline().strip()
                if line.startswith("."):
                    break
                line = line.split(" ")
                key = int(line[0])
                lesson_time = time.strptime(line[1], "%H:%M")
                self.lessons_start_time[key] = lesson_time

            lessons = None
            while True:
                line = file.readline()
                if line == "":
                    break
                line = line.strip()
                if line.startswith(">"):
                    lessons = {}
                elif line.startswith("."):
                    self.schedule.append(lessons)
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


