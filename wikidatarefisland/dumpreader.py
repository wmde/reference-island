import gzip
import json


class DumpReader(object):
    def __init__(self, path):
        self.path = path

    def check_data(self, line):
        try:
            item = json.loads(line.replace('\n', '')[:-1])
        except:
            # It's not using json-lines, it's a big json thus this mess.
            return
        if item['type'] != 'item':
            return
        return item

    def read_items(self):
        with gzip.open(self.path, 'rt') as f:
            for line in f:
                item = self.check_data(line)
                if item is None:
                    continue

                yield item
