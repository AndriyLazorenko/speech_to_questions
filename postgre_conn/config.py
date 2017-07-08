from configparser import ConfigParser
import os
from os.path import join


CURRENT_PATH = os.path.dirname(__file__)
FILENAME = 'database.ini'
PATH = join(CURRENT_PATH, FILENAME)


def config(path=PATH, section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(path)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, FILENAME))

    return db

