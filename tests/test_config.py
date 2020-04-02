import os

from wikidatarefisland import Config


def test_config_simple():
    config = Config({'foo': 'bar'})
    assert config.get('foo') == 'bar'


def test_from_script_path():
    config = Config.newFromScriptPath(os.path.realpath(__file__))
    assert config.get('data_storage_path') == 'data/'
