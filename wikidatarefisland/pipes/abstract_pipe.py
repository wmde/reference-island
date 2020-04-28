from abc import ABC, abstractmethod
from typing import Iterable

LineList = Iterable[dict]


class AbstractPipe(ABC):
    @abstractmethod
    def flow(self, data: dict) -> LineList:
        raise NotImplementedError
