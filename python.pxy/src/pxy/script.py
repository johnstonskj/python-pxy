"""
Script methods, these are used by setuptools to create platform-specific 
executable scripts.

Each script takes parameters of the form:
  script [(inp-file|stdin) [out-file|stdout]]
"""

import sys
from xml.etree import ElementTree

import pxy, pxy.pxml

def __usage():
    import os.path
    name = os.path.basename(sys.argv[0])
    print 'Usage: %s [(inp-file|stdin) [out-file|stdout]]' % name

def pxy_to_xml():
    if len(sys.argv) > 3:
        __usage()
        return
    # Process input
    dict = {}
    if len(sys.argv) >= 2:
        dict = pxy.parse(sys.argv[1]) 
    else:
        dict = pxy.parse(sys.stdin)
    # Convert
    xml = pxy.pxml.to_string(dict)
    # And Output
    out = sys.stdout
    close_out = False
    if len(sys.argv) == 3:
        out = open(sys.argv[2], 'wt')
        close_out = True
    out.write(xml)
    if close_out:
        out.close()

def xml_to_pxy():
    if len(sys.argv) > 3:
        __usage()
        return
    # Process input
    etree = None
    inp = sys.stdin
    if len(sys.argv) >= 2:
        etree = ElementTree.parse(sys.argv[1])
    else:
        etree = ElementTree.parse(sys.stdin)
    # Convert
    dict = pxy.pxml.from_etree(etree)
    # And Output
    out = sys.stdout
    close_out = False
    if len(sys.argv) == 3:
        out = open(sys.argv[2], 'wt')
        close_out = True
    out.write(pxy.to_string(dict))
    if close_out:
        out.close()
