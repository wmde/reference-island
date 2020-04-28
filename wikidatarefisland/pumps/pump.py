from abc import ABC, abstractmethod
from wikidatarefisland.data_access import Storage
from wikidatarefisland.pipes import AbstractPipe


class AbstractPump(ABC):
    @abstractmethod
    def run(self, pipe: AbstractPipe, input_file_path: str, output_file_path: str) -> None:
        raise NotImplementedError


class SimplePump(AbstractPump):
    def __init__(self, storage: Storage):
        self.storage = storage

    def run(self, pipe: AbstractPipe, input_file_path: str, output_file_path: str):
        for line in self.storage.getLines(input_file_path):
            output = pipe.flow(line)
            for single_output in output:
                # TODO: we're opening and closing this on every single line of output
                self.storage.append(output_file_path, single_output)
