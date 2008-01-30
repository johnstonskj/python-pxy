"""
PXY XML functions, converts between XML and PXY.
"""

import StringIO, types
from xml.sax.saxutils import XMLGenerator
from xml.etree import ElementTree

import pxy

__DEFAULT_ENCODING = 'utf-8'

def to_xml_string(pxy):
    """ to_xml_string(pxy) -> str
        Convert the PXY string into an XML string. 
    """
    if type(pxy) == type({}):
        for key,value in pxy.iteritems():
            element = __to_xml(key, value, None)
        return '<?xml version="1.0" encoding="%s"?>%s' % (__DEFAULT_ENCODING,
                                                          ElementTree.tostring(element, __DEFAULT_ENCODING))
    else:
        raise pxy.InvalidFileFormatException, "expecting string or dictionary, not %s" % str(type(pxy))

def to_etree(pxy):
    """ to_etree(pxy) -> ElementTree
        Convert the PXY string into an ElementTree.
    """
    xml = to_xml_string(pxy)
    return ElementTree.XML(xml)

def from_xml_string(xml):
    """ from_xml_string(xml) -> str
        Convert the XML string into a dictionary structure.
    """
    return from_etree(ElementTree.XML(xml))

def from_etree(etree):
    """ from_etree(etree) -> str
        Convert the ElementTree into a dictionary structure.
    """
    raise NotImplementedError

def __to_xml(key, value, element):
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
            __to_xml(key2, value2, element)
        elif type(value2) in pxy.__LIST_TYPES:
            for item in value2:
                if type(item) in pxy.__SIMPLE_TYPES:
                    child = ElementTree.SubElement(element, key2)
                    child.text = str(item)
                else: 
                    __to_xml(key2, item, element)
    return element