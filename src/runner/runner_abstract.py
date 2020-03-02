from abc import ABC, abstractmethod


class RunnerAbstract(ABC):
    def __init__(self):
        self._data = {"message": "job has not been executed"}
        self._status = 200

    @property
    def response(self):
        return self._data, self._status

    @abstractmethod
    def execute(self, job):
        pass
