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
                try:
                    # TODO Fix this hack to make json behave a bit like jsonl: T251271
                    yield json.loads(line.strip().strip(','))
                except json.JSONDecodeError:
                    continue

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
            if raw:
                f.write(value)
            else:
                # Add newline if file is not empty
                new_line = '\n' if os.stat(f.name).st_size else ''
                f.write(new_line + json.dumps(value, ensure_ascii=False))

    @classmethod
    def newFromScript(cls, path):
        data_path = os.path.join(os.path.dirname(path), '../data/')
        return cls(data_path)
