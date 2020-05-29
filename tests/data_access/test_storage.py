import bz2
import gzip
import json
import os

from wikidatarefisland.data_access import Storage


class TestStorage:
    def test_instantiate(self, tmp_path):
        storage = Storage(tmp_path)
        assert isinstance(storage, Storage)
        assert storage.path is tmp_path

    def test_newFromScript(self, tmp_path):
        data_path = os.path.join(os.path.dirname(tmp_path), '../data/')
        storage = Storage.newFromScript(tmp_path)
        assert storage.path == data_path

    def test_get(self, tmpdir):
        mock_file = tmpdir.join('test.json')
        mock_file.write(json.dumps({"test": "hello"}))

        storage = Storage(tmpdir)

        assert storage.get("test.json") == json.loads(mock_file.read())

    def test_get_dump_lines_json(self, tmpdir):
        mock_lines = [
            {"test": "hello"},
            {"goodbye": "test"}
        ]

        mock_data = '''
        [
            {"test": "hello"},
            {"goodbye": "test"}
        ]
        '''

        mock_file = tmpdir.join('test.json')
        mock_file.write(mock_data)
        path = os.path.join(tmpdir, 'test.json')

        storage = Storage(tmpdir)

        assert list(storage.get_dump_lines(path)) == mock_lines

    def test_get_dump_lines_gz(self, tmpdir):
        mock_lines = [
            {"test": "hello"},
            {"goodbye": "test"}
        ]

        mock_data = '''
        [
            {"test": "hello"},
            {"goodbye": "test"}
        ]
        '''
        path = os.path.join(tmpdir, 'test.json.gz')
        with gzip.open(path, 'w') as f:
            f.write(bytes(mock_data, 'utf-8'))

        storage = Storage(tmpdir)

        assert list(storage.get_dump_lines(path)) == mock_lines

    def test_get_dump_lines_bz2(self, tmpdir):
        mock_lines = [
            {"test": "hello"},
            {"goodbye": "test"}
        ]

        mock_data = '''
            [
                {"test": "hello"},
                {"goodbye": "test"}
            ]
            '''

        path = os.path.join(tmpdir, 'test.json.bz2')
        with bz2.open(path, 'w') as f:
            f.write(bytes(mock_data, 'utf-8'))

        storage = Storage(tmpdir)

        assert list(storage.get_dump_lines(path)) == mock_lines

    def test_getLines_jsonl(self, tmpdir):
        mock_lines = [
            {"test": "hello"},
            {"goodbye": "test"}
        ]

        mock_file = tmpdir.join('test.jsonl')
        mock_file.write("\n".join(map(lambda l: json.dumps(l), mock_lines)))

        storage = Storage(tmpdir)

        assert list(storage.getLines('test.jsonl')) == mock_lines

    def test_store_raw(self, tmpdir):
        storage = Storage(tmpdir)
        storage.store('test.txt', "Hello", True)

        assert tmpdir.join('test.txt').read() == "Hello"

    def test_store_json(self, tmpdir):
        mock_dict = {"hello": "test"}
        storage = Storage(tmpdir)
        storage.store('test.json', mock_dict)

        assert tmpdir.join('test.json').read() == json.dumps(mock_dict)

    def test_append_raw(self, tmpdir):
        mock_file = tmpdir.join('test.txt')
        mock_file.write('Hello')

        storage = Storage(tmpdir)
        storage.append('test.txt', 'Goodbye', True)

        assert mock_file.read() == 'Hello\nGoodbye'

    def test_append_json(self, tmpdir):
        mock_lines = [
            {"hello": "test"},
            {"goodbye": "test"}
        ]

        mock_file = tmpdir.join('test.json')
        mock_file.write(json.dumps(mock_lines[0]))

        expected = '\n'.join(map(lambda l: json.dumps(l), mock_lines))

        storage = Storage(tmpdir)
        storage.append("test.json", mock_lines[1])

        assert mock_file.read() == expected

    def test_append_json_empty(self, tmpdir):
        mock_line = {"hello": "test"}
        mock_file = tmpdir.join('test.json')

        storage = Storage(tmpdir)
        storage.append("test.json", mock_line)

        assert mock_file.read() == json.dumps(mock_line)
