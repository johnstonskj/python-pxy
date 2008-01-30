"""
Test the basic pxy module
"""

import pprint, unittest

import tdata, pxy

class BasicTranslationUnitTests(unittest.TestCase):
    """
    Test translation between PXY strings and Python dictionaries
    """
    
    def testBadDictionaries(self):
        for dict in tdata.BAD_DICTS:
            self.assertRaises(pxy.InvalidFileFormatException, pxy.to_string, dict)
            
    def testWriteBasicDirectionaries(self):
        for dict in tdata.GOOD_DICTS:
            pxy.write(dict)
            
    def testToStringBasicDirectionaries(self):
        for dict in tdata.GOOD_DICTS:
            print pxy.to_string(dict)
            
    def testParseStrings(self):
        for text in tdata.GOOD_PXY:
            pprint.pprint(pxy.parse_string(text))
