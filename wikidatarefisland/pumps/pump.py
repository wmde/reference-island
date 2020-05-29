import json
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
                self.storage.append(output_file_path, single_output)


class DumpReaderPump(AbstractPump):
    """Pump for reading Wikidata JSON Entity Dumps and writing the output line by line

    Pump that works at scale to read from Wikidata JSON Entity Dumps.
    It can take either uncompressed or gzip or bzip2 formatted data
    but it must contain one complete item per line.

    Any malformed input lines are silently ignored.

    Writing is batched such that each batch is at least as big as batch_size
    """
    def __init__(self, storage: Storage, batch_size: int):
        self.storage = storage
        self.batch_size = batch_size

    def run(self, pipe: AbstractPipe, input_file_path: str, output_file_path: str):
        values = []
        for line in self.storage.get_dump_lines(input_file_path):
            output = pipe.flow(line)
            for single_output in output:
                values.append(json.dumps(single_output, ensure_ascii=False))
                if len(values) >= self.batch_size:
                    self.storage.append(output_file_path, '\n'.join(values), raw=True)
                    values = []
        self.storage.append(output_file_path, '\n'.join(values), raw=True)


class ObserverPump(AbstractPump):
    """ Sneaky pump that doesn't write output and only observers and measures."""
    def __init__(self, storage: Storage):
        self.storage = storage

    def run(self, pipe: AbstractPipe, input_file_path: str, output_file_path: str):
        for line in self.storage.getLines(input_file_path):
            pipe.flow(line)
