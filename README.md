Simple Python-like syntax for expressing hierarchical data and tools to convert between PXY and XML. The purpose was to provide a simple syntax that can easily be written without the <>. Writing large amounts of XML on whiteboards, or even in discussion documents, let alone IM is time consuming and we find ourselves writing "short forms"

# Status

Currently about alpha, the basic tests execute but there is work to do on the parser and the setup script.

# Example

    document:
        element:
        number=1
        string='something'
        'element content'
        {namespace}child: 'simple content'

# See also

SLip http://www.scottsweeney.com/projects/slip
http://www.ibm.com/developerworks/xml/library/x-syntax.html
