"""
Script methods, these are used by setuptools to create platform-specific 
executable scripts.
"""

import sys
import pxy, pxy.pxml

def pxy_to_xml():
    inp = sys.stdin
    out = sys.stdout
    close_out = False
    dict = {}
    if len(sys.argv) == 3:
        dict = parse(sys.argv[2])
    if len(sys.argv) == 2:
        inp = fopen(sys.argv[1], 'wt')
        
    if close_out:
        out.close()
    if close_inp:
        inp.close()

def xml_to_pxy():
    pass