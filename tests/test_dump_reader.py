import os

from wikidatarefisland.dump_reader import DumpReader


def test_dump_reader():
    dir_ = os.path.dirname(os.path.realpath(__file__))
    dump_reader = DumpReader(os.path.join(dir_, 'one-entity-dump.json.gz'))
    items = list(dump_reader.read_items())
    assert len(items) == 1
    assert items[0]['id'] == 'Q7251'
