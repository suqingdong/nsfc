import os
import json
import codecs


BASE_DIR = os.path.dirname(os.path.realpath(__file__))
version_file = os.path.join(BASE_DIR, 'version', 'version.json')
version_info = json.load(codecs.open(version_file, encoding='utf-8'))

__version__ = version_info['version']

DEFAULT_DB = os.path.join(BASE_DIR, 'data', 'proejct.db')
HOME = os.path.expanduser('~')

if not os.path.isfile(DEFAULT_DB):
    file = os.path.join(HOME, 'nsfc_data', 'project.db')
    if os.path.isfile(file):
        DEFAULT_DB = file
