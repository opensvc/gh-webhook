from abc import ABC, abstractmethod


class ContextAbstract(ABC):
    @property
    def description(self) -> dict:
        return dict({})

    @property
    @abstractmethod
    def event(self):
        pass

    @property
    @abstractmethod
    def name(self):
        pass
