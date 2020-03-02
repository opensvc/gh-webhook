from runner.http_abstract import HttpRunnerAbstract


class Runner(HttpRunnerAbstract):
    def __init__(self):
        super().__init__('post')
