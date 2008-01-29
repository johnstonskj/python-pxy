import pprint, unittest

import tdata, pxy, pxy.pxml

class XmlTranslationUnitTests(unittest.TestCase):
    
    def testToStringBasicDirectionaries(self):
        for dict in tdata.GOOD_DICTS:
            print pxy.pxml.to_xml_string(dict)
            
    def testParseToStringBasicStrings(self):
        for text in tdata.GOOD_PXY:
            print pxy.pxml.to_xml_string(pxy.parse_string(text))
            
    def testParseToStringQualifiedString(self):
        dict = pxy.parse_string(tdata.QUALIFIED_PXY)
        print pxy.pxml.to_xml_string(dict)
