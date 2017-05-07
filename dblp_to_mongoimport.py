import json

from bson import json_util

from converter import xml_converter
from utils import *


def convert_element(tag, value):
    maybe_convert_date(value, 'mdate')
    maybe_convert_int(value, 'year')

    value['tag'] = tag

    if 'author' in value:
        if isinstance(value['author'], str):
            value['author'] = [value['author']]

        value['num_authors'] = len(value['author'])

    return json.dumps(value, default=json_util.default)


tags = ('article', 'inproceedings', 'proceedings', 'book', 'incollection', 'phdthesis', 'mastersthesis', 'www')

with open('output/dblp.json', 'w') as out:
    for _, element in xml_converter('input/dblp.xml', {'tag': tags, 'load_dtd': True}, convert_element):
        out.write(element)
        out.write("\n")
