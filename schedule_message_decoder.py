import datetime
import schedule_question
import re


def is_in(container, *args):
    for arg in args:
        if arg in container:
            return True
    return False


class MessageDecoder:
    def __init__(self, timezone):
        self.timezone = timezone
        self.question = None

    def decode_message(self, message):
        message = str(message).lower().strip()
        if not message.startswith("бот " or "бот," or "бот!" or "бот:"):
            return

        self.question = schedule_question.Question()

        message = message[4:]
        message = re.sub(r"\d", " ", message)
        words = [word for word in re.split("\W", message) if word != ""]

        # todo
        return Question()



    def decode_datetime(self, words, question):
        now = datetime.datetime.utcnow()
        timezone_shift = datetime.timedelta()
        timezone_shift.seconds = 3600 * self.timezone
        now = now + timezone_shift

        if is_in(words, "прошлая", "прошлый", "прошлом", "предыдущей", "предыдущем"):
            question.time_type = TimeType.previous
        elif is_in(words, "прошли", "были"):
            question.time_type = TimeType.was
        elif is_in(words, "прошли", "были"):
            question.time_type = TimeType.was

        if "сегодня" in words:
            question.datetime = now
        elif "завтра" in words:
            question.datetime = now + datetime.timedelta(1)
        else:
            weekdays = self.schedule.get_weekdays()
            weekdays_short = [weekday[:-1].lower() for weekday in weekdays]
            for weekday_number in range(len(weekdays_short)):
                weekday = weekdays_short[weekday_number]
                for word in words:
                    if weekday in word:
                        now.weekday()
                        question.datetime

