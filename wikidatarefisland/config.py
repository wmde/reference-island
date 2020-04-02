import os

import yaml


class Config(object):
    def __init__(self, configs):
        self.configs = configs

    def get(self, config):
        return self.configs.get(config)

    @classmethod
    def newFromScriptPath(cls, path):
        data_path = os.path.join(os.path.dirname(path), '../config/')
        return cls.newFromPath(data_path)

    @classmethod
    def newFromPath(cls, path):
        defaults_path = os.path.join(path, 'default.yml')
        overrides_path = os.path.join(path, 'override.yml')
        with open(defaults_path, 'r') as f:
            configs = yaml.load(f.read(), Loader=yaml.FullLoader)
        with open(overrides_path, 'r') as f:
            overrides = yaml.load(f.read(), Loader=yaml.FullLoader)
        if overrides:
            for config in overrides:
                configs[config] = overrides[config]

        return cls(configs)
