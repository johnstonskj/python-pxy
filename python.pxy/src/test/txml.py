"""
Test the pxy.pxml module
"""

import pprint, unittest

import tdata, pxy, pxy.pxml

class XmlTranslationUnitTests(unittest.TestCase):
    """
    Test translation between PXY strings and XML, using ElementTree
    """
    
    def testToStringBasicDirectionaries(self):
        for dict in tdata.GOOD_DICTS:
            print pxy.pxml.to_xml_string(dict)
            
    def testParseToStringBasicStrings(self):
        for text in tdata.GOOD_PXY:
            print pxy.pxml.to_xml_string(pxy.parse_string(text))
            
    def testParseToStringQualifiedString(self):
        dict = pxy.parse_string(tdata.QUALIFIED_PXY)
        print pxy.pxml.to_xml_string(dict)
