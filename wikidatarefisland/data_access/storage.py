import bz2
import gzip
import json
import os


class Storage(object):
    def __init__(self, path):
        self.path = path

    def get(self, file_):
        path = os.path.join(self.path, file_)
        with open(path, 'r') as f:
            return json.loads(f.read())

    def getLines(self, file_):
        path = os.path.join(self.path, file_)
        with open(path, 'r') as f:
            for line in f:
                yield json.loads(line.strip())

    def get_dump_lines(self, path):
        mode = 'r'
        file_ = os.path.split(path)[-1]
        if file_.endswith('.gz'):
            f = gzip.open(path, mode)
        elif file_.endswith('.bz2'):
            f = bz2.BZ2File(path, mode)
        elif file_.endswith('.json'):
            f = open(path, mode)
        else:
            raise NotImplementedError(f'Reading file {file_} is not supported')
        try:
            for line in f:
                if isinstance(line, bytes):
                    line = line.decode('utf-8')
                try:
                    yield json.loads(line.strip().strip(','))
                except json.JSONDecodeError:
                    continue
        finally:
            f.close()

    def store(self, file_, value, raw=False):
        path = os.path.join(self.path, file_)
        with open(path, 'w') as f:
            if raw:
                f.write(value)
            else:
                f.write(json.dumps(value, ensure_ascii=False))

    def append(self, file_, value, raw=False):
        path = os.path.join(self.path, file_)
        with open(path, 'a') as f:
            # Add newline if file is not empty
            new_line = '\n' if os.stat(f.name).st_size else ''
            if raw:
                f.write(new_line + value)
            else:
                f.write(new_line + json.dumps(value, ensure_ascii=False))

    @classmethod
    def newFromScript(cls, path):
        data_path = os.path.join(os.path.dirname(path), '../data/')
        return cls(data_path)
