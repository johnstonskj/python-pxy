"""
Test the pxy.pxml module
"""

import pprint, unittest
from xml.etree import ElementTree

import tdata, pxy, pxy.pxml

class XmlTranslationUnitTests(unittest.TestCase):
    """
    Test translation between PXY strings and XML, using ElementTree
    """
    
    def testToStringBasicDirectionaries(self):
        for dict in tdata.GOOD_DICTS:
            print pxy.pxml.to_string(dict)
            
    def testParseToStringBasicStrings(self):
        for text in tdata.GOOD_PXY:
            print pxy.pxml.to_string(pxy.parse_string(text))
            
    def testParseToStringQualifiedString(self):
        for text in tdata.QUALIFIED_PXY:
            dict = pxy.parse_string(text)
            print pxy.pxml.to_string(dict)

    def testFromXml(self):
        for text in tdata.GOOD_XML:
            dict = pxy.pxml.from_etree(ElementTree.XML(text))
            print pxy.pxml.to_string(dict)
    
    def testFromETree(self):
        root = ElementTree.Element('root', {})
        child = ElementTree.SubElement(root, 'child', {'foo': 'bar'})
        child.text = 'child 1'
        child = ElementTree.SubElement(root, 'child', {'foo': 'bar'})
        child.text = 'child 2'
        child = ElementTree.SubElement(child, 'child', {'foo': 'bar'})
        child.text = 'child 3'
        dict = pxy.pxml.from_etree(root)
        pprint.pprint(dict)
        print pxy.to_string(dict)
