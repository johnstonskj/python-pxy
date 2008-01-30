"""
PXY XML functions, converts between XML and PXY.
"""

import StringIO, types
from xml.sax.saxutils import XMLGenerator
from xml.etree import ElementTree

import pxy

__DEFAULT_ENCODING = 'utf-8'

def to_string(dict):
    """ to_string(dict) -> str
        Convert the PXY dictionary into an XML string. 
    """
    etree = to_etree(dict)
    if etree is None:
        return ""
    else:
        return '<?xml version="1.0" encoding="%s"?>%s' % (__DEFAULT_ENCODING,
                                                          ElementTree.tostring(etree, __DEFAULT_ENCODING))

def to_etree(dict):
    """ to_etree(dict) -> ElementTree
        Convert the PXY dictionary into an ElementTree.
    """
    if type(dict) == type({}):
        root = {}
        for key,value in dict.iteritems():
            root = __to_etree(key, value, None)
        return root
    else:
        raise pxy.InvalidFileFormatException, "expecting string or dictionary, not %s" % str(type(pxy))

def from_string(xml):
    """ from_xml_string(xml) -> str
        Convert the XML string into a dictionary structure.
    """
    return from_etree(ElementTree.XML(xml))

def from_etree(etree):
    """ from_etree(etree) -> str
        Convert the ElementTree into a dictionary structure.
    """
    element = ElementTree.Element('dummy')
    if isinstance(etree, ElementTree.ElementTree):
        return __from_etree(etree.getroot(), {})
    elif isinstance(etree, type(element)):
        return __from_etree(etree, {})
    else:
        raise pxy.InvalidFileFormatException, 'etree not ElementTree or Element'

def __to_etree(key, value, element):
    """ __to_etree(key, value, element) -> Element
        Recursive function to build an ElementTree from a dictionary.
    """
    attributes = {}
    for key2,value2 in value.iteritems():
        if type(value2) in pxy.__SIMPLE_TYPES:
            if key2:
                attributes[key2] = str(value2)
    if element is None:
        element = ElementTree.Element(key, attributes)
    else:
        element = ElementTree.SubElement(element, key, attributes)
    if value.has_key(''):
        element.text = str(value[''])
    for key2,value2 in value.iteritems():
        if type(value2) == types.DictType:
            __to_etree(key2, value2, element)
        elif type(value2) in pxy.__LIST_TYPES:
            for item in value2:
                if type(item) in pxy.__SIMPLE_TYPES:
                    child = ElementTree.SubElement(element, key2)
                    child.text = str(item)
                else: 
                    __to_etree(key2, item, element)
    return element

def __from_etree(etree, dict):
    """ __from_etree(etree) -> dict
        Recursive function to build a dictionary from an ElementTree Element.
    """
    new = {}
    if dict.has_key(etree.tag):
        elem = dict[etree.tag]
        dict[etree.tag] = [elem,new]
    else:
        dict[etree.tag] = new
    for attr in etree.keys():
        new[attr] = etree.get(attr)
    if etree.text and etree.tag:
        new[''] = etree.text
    for child in list(etree):
        __from_etree(child, new)
    return dict
