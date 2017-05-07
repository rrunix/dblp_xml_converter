from collections import defaultdict


def xml_converter(filename, etree_args=None, element_converter=None):
    """
    Convert a xml file into a generator of dictionaries. The converter is suitable for large xml when there 
    are a lot of small elements (the element needs to fit in memory) hanging from the root node.
    
    
    If a element_converter is provided, then the converter is applied before the element is yielded.
    
    :param filename: The filename of the xml to convert
    :param etree_args: Args to etree.iterparse converter (http://lxml.de/api/lxml.etree.iterparse-class.html)
    :param element_converter: function (tag to convert, value to converter), where the tag is the element name
    :return: None
    """

    from lxml import etree
    context = etree.iterparse(filename, **etree_args)
    element_converter = element_converter or (lambda x, y: y)

    def node2dict(element):
        items = defaultdict(list)
        items.update(element.attrib)

        if len(element) > 0:
            for sub_element in element:
                items[sub_element.tag].append(node2dict(sub_element))

            return {k: v[0] if len(v) == 1 else v for k, v in items.items()}

        return element.text

    for _, elem in context:
        elem_dict = node2dict(elem)
        tag = elem.tag
        elem.clear()

        yield tag, element_converter(tag, elem_dict)
