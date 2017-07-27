import getopt
from configparser import ConfigParser

import sys


class Config:
    URL = 'http://localhost:8000'
    HTTP_TIMEOUT = 10

    def __init__(self):
        rules = self.get_rules()

        for rule in rules:
            setattr(self, rule, rules.getint(rule))

    def get_config_filename(self):
        filename = 'config.ini'

        opts, _ = getopt.getopt(sys.argv[1:], 'c:', ['config='])
        for opt, arg in opts:
            if opt == '-c':
                filename = arg

        return filename

    def get_rules(self):
        config_parser = ConfigParser()
        config_parser.read(self.get_config_filename())
        try:
            return config_parser['RULES']
        except KeyError:
            raise ValueError('Config file not valid')

config = Config()
