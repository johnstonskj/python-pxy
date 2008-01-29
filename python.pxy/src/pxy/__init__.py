"""
PXY (pronounded Pixie) is a simple file format that allows a structured
representation of data and is easily and directly translated into XML. 

Examples

app:
    name = 'Me'
    description = 'my thing'
    version:
        major = 1
        build = 'darwin'
        minor = 0

<app name="Me" description="my thing">
  <version major="1" minor="0" build="darwin">
</app>

app:
    version:
        major:
            1
        build:
            'darwin'
        minor:
            0
    name: 'Me'
    description: 'my thing'
        
<app>
  <name>Me</name>
  <description>my thing</description>
  <version>
    <major>1</major>
    <minor>0</minor>
    <build>darwin</build>
  </version>
</app>
  
"""

import re, sys, types
import StringIO

__version__ = '1.0'
__author__ = 'Simon Johnston'
__author_email__ = 'skjohn@us.ibm.com'

__INDENT = '    '
__SIMPLE_TYPES = [types.BooleanType, types.FloatType, types.IntType, types.LongType, 
                  types.StringType, types.UnicodeType]
__LIST_TYPES = [types.ListType, types.TupleType]

__RE_QNAME = re.compile('^{(P<ns>\w+)}(P<name>\w+)$')
__RE_OBJ = re.compile('^(\s*)(({[^}]+})?\w+):\s*$') #('^(P<lws>\s*)(P<name>\w+):\s*')
__RE_OBJ2 = re.compile('^(\s*)(({[^}]+})?\w+):\s*(.*)') #('^(P<lws>\s*)(P<name>\w+):\s*')
__RE_ATTR = re.compile('^(\s*)(({[^}]+})?\w+)\s*=\s*(.*)') #('^(P<lws>\s*)(P<name>\w+)\s*=\s*(P<value>\S+)\s*$')
__RE_CONTENT = re.compile('^(\s*)(.*)') #('^(P<lws>\s*)(P<value>\S+)\s*$')

class InvalidFileFormatException(Exception):
    """ This is raised on specific file formatting issues where a string
        or file does not match the PXY format.
    """
    pass

def parse(file):
    """ parse(file) -> dict
        Parse the file from PXY into a dictionary. file may be a string containing
        the fil name or may be a file handle.
    """
    fh = file
    if type(file) == type(""):
        fh = open(file, "rt")
        do_close = True
    pxy = ""
    for line in fh:
        pxy = pxy + line
    if do_close:
        fh.close()
    return parse_string(pxy)

def parse_string(pxy):
    """ parse_string(pxy) -> dict
        Parse the presented PXY string into a dictionary.
    """
    # TODO: Currently doesn't unwind stack correctly!
    stack = []
    current = {}
    stack.append(current)
    last_indent = 0
    expect_indent = 0
    lines = pxy.split('\n')
    for line in lines:
        if len(line) > 0:
            m_obj = __RE_OBJ.match(line)
            m_obj2 = __RE_OBJ2.match(line)
            m_attr = __RE_ATTR.match(line)
            m_content = __RE_CONTENT.match(line)
            if m_obj:
                if len(m_obj.group(1)) < last_indent:
                    stack.pop()
                    current = stack[len(stack)-1]
                last_indent = len(m_obj.group(1))
                new = {}
                if current.has_key(m_obj.group(2)):
                    elem = current[m_obj.group(2)]
                    if type(elem) in __SIMPLE_TYPES:
                        raise InvalidFileFormatException, 'Cannot have attribute/element with same name'
                    elif type(elem) == types.ListType:
                        elem.append(new)
                    else:
                        current[m_obj.group(2)] = [new,]
                else:
                    current[m_obj.group(2)] = new
                current = new
                stack.append(new)
                expect_indent = 1
            elif m_obj2:
                if len(m_obj2.group(1)) < last_indent:
                    stack.pop()
                    current = stack[len(stack)-1]
                last_indent = len(m_obj2.group(1))
                new = {}
                new[''] = m_obj2.group(3)
                if current.has_key(m_obj2.group(2)):
                    elem = current[m_obj2.group(2)]
                    if type(elem) in __SIMPLE_TYPES:
                        raise InvalidFileFormatException, 'Cannot have attribute/element with same name'
                    elif type(elem) == types.ListType:
                        elem.append(new)
                    else:
                        current[m_obj2.group(2)] = [elem,new]
                else:
                    current[m_obj2.group(2)] = new
                expect_indent = 0
            elif m_attr:
                if expect_indent and len(m_attr.group(1)) <= last_indent:
                    raise IndentationError
                last_indent = len(m_attr.group(1))
                if current.has_key(m_attr.group(2)):
                    raise InvalidFileFormatException, 'Cannot have more than one attribute with the same name'
                current[m_attr.group(2)] = eval(m_attr.group(4))
                expect_indent = 0
            elif m_content:
                if expect_indent and len(m_content.group(1)) <= last_indent:
                    raise IndentationError
                last_indent = len(m_content.group(1))
                if current.has_key(''):
                    raise InvalidFileFormatException, 'Only one content node allowed per element' 
                current[''] = eval(m_content.group(2))
                expect_indent = 0
            else:
                raise InvalidFileFormatException, 'Badly formatted line: %s' % line
    return stack[0]

def to_string(dict):
    """ to_string(dict) -> str
        Convert the dictionary structure into a PXY string.
    """
    fh = StringIO.StringIO()
    write(dict, fh)
    string = fh.getvalue()
    fh.close()
    return string

def write(dict, fh=sys.stdout):
    """ write(dict, fh=sys.stdout)
        Write the dictionary structure out to a file as a PXY string.
    """
    if len(dict.keys()) > 1:
        raise InvalidFileFormatException, "root dictionary should have just one entry"
    key = dict.keys()[0]
    obj = dict.get(key)
    __write(key, obj, fh, "")
    
def __write(name, obj, fh, indent):
    if type(obj) == types.DictionaryType:
        fh.write("%s%s:\n" % (indent, name))
        for key,value in obj.iteritems():
            if type(value) in __SIMPLE_TYPES:
                if key:
                    fh.write("%s%s = %s\n" % (indent+__INDENT, key, repr(value)))
                else:
                    fh.write("%s%s\n" % (indent+__INDENT, repr(value)))
        for key,value in obj.iteritems():
            if not type(value) in __SIMPLE_TYPES:
                __write(key, value, fh, indent+__INDENT)
    elif type(obj) in __LIST_TYPES:
        for item in obj:
            if type(item) in __SIMPLE_TYPES:
                fh.write("%s%s:\n" % (indent, name))
                __write(name, item, fh, indent+__INDENT)
            else:
                __write(name, item, fh, indent)
    elif type(obj) in __SIMPLE_TYPES:
        fh.write("%s%s\n" % (indent, repr(obj)))
    else:
        raise InvalidFileFormatException, "unexpected type, %s" % str(type(obj))
