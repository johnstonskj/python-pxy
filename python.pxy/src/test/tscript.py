"""
Test the command-line scripts
"""

import os, os.path, unittest

import tdata, pxy, pxy.pxml

class ScriptTests(unittest.TestCase):
    """
    Test generated scripts
    """
    
    def testPxy2Xml(self):
        (path,file) = os.path.split(__file__)
        os.system('pxy2xml %s%s%s' % (path, os.sep, 'example.pxy'))
            
    def testXml2Pxy(self):
        (path,file) = os.path.split(__file__)
        os.system('xml2pxy %s%s%s' % (path, os.sep, 'example.pxy'))
