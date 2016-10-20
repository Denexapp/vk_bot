class Question:
    def __init__(self):
        self.time_type = None
        self.question_type = Question.QuestionType.incorrect
        self.day = None
        self.time = None

        self.lesson_number = None

    class QuestionType:
        incorrect = -1
        teacher = 0
        where = 1
        amount = 2
        which = 3
        even = 4
        help = 5

    class TimeType:
        # время/пара
        was = -2
        previous = -1
        at_time = 0
        next = 1
        left = 2
        all = 3
