from runner.runner_abstract import RunnerAbstract


class Runner(RunnerAbstract):
    def execute(self, job):
        self._data = {'message': f'nothing to do on name:{job.context.name}, event: {job.context.event}'}
