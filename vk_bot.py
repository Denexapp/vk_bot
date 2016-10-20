import curio


class VkBot:
    def __init__(self, api, queue):
        self.api = api
        self.queue = queue

    @terminate_on_error
    async def run(self):
        pass


def terminate_on_error(function):
    def new_function(*args, **kwargs):
        try:
            print("DECORATOR")
            function(*args, **kwargs)
        except curio.TaskError:
            raise Exception
    return new_function
