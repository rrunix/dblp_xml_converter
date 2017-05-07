from converter import xml_converter
from utils import *
import csv

CSV_SEPARATOR = ','
publication_headers = ['key', 'year', 'tag', 'author']


def convert_element(tag, value, curr_id=[0]):

    curr_id[0] += 1
    value['key'] = ("%s_%s" %(value['key'], str(curr_id[0]))).upper()
    value['tag'] = tag
    maybe_convert_int(value, 'year')

    if 'author' in value:
        if isinstance(value['author'], str):
            authors = [value['author']]
        else:
            authors = value['author']
    else:
        authors = ['']

    value['author'] = ';'.join(authors)

    return format_publication(value)


def format_publication(value):
    res = [''] * len(publication_headers)

    for i, header in enumerate(publication_headers):
        if header in value:
            res[i] = value[header]

    return res

tags = ('article', 'inproceedings', 'proceedings', 'book', 'incollection', 'phdthesis', 'mastersthesis', 'www')

with open('output/publications.csv', 'w') as pub_out:
    pub_out_writter = csv.writer(pub_out, delimiter=CSV_SEPARATOR, quotechar='|', quoting=csv.QUOTE_MINIMAL)

    pub_out_writter.writerow(publication_headers)
    for _, element in xml_converter('input/dblp.xml', {'tag': tags, 'load_dtd': True}, convert_element):
        pub_out_writter.writerow(element)
