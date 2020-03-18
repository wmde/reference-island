import json
import os


class Storage(object):
    def __init__(self, path):
        self.path = path

    def get(self, file_):
        path = os.path.join(self.path, file_)
        with open(path, 'r') as f:
            return json.loads(f.read())

    def store(self, file_, value):
        path = os.path.join(self.path, file_)
        with open(path, 'w') as f:
            f.write(json.dumps(value))

    def append(self, file_, value):
        path = os.path.join(self.path, file_)
        with open(path, 'a') as f:
            f.write(json.dumps(value))

    @classmethod
    def newFromScript(cls, path):
        data_path = os.path.join(os.path.dirname(path), '../data/')
        return cls(data_path)
