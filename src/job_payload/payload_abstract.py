from abc import ABC, abstractmethod

from context.context_abstract import ContextAbstract


class PayloadProviderAbstract(ABC):
    @staticmethod
    @abstractmethod
    def __call__(context: ContextAbstract):
        pass
