from initxyz.utils import write_file
from configparser import ConfigParser
from io import StringIO
from os.path import exists

class ConfigFile:
    def __init__(self, path):
        self.path = path
        self.data = ConfigParser()
        if exists(path):
            self.data.read(path)

    def has_option(self, section, key):
        return self.data.has_option(section, key)

    def get(self, section, key, **kwargs):
        return self.data.get(section, key, **kwargs)

    def set(self, section, key, value):
        if not self.data.has_section(section):
            self.data.add_section(section)

        self.data.set(section, key, value)

        out = StringIO()
        self.data.write(out)
        write_file(path=self.path, data=out.getvalue().encode('utf-8'))
