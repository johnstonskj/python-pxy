BAD_DICTS = [{'app1': 'ok', 'app2': 'bad'}
            ]

GOOD_DICTS = [{'app': {'name': 'Me', 'version': '1.0'}},
              {'app': {'name': 'Me', 'version': {'major': 1, 'minor': 0, 'build': 'darwin'}, 'description': 'my thing'}},
              {'app': {'name': {'': 'Me'}, 'version': {'major': {'': 1}, 'minor': {'': 0}, 'build': {'': 'darwin'}}, 'description': {'': 'my thing'}}},
              {'app': {'name': 'Me', 'version': '1.0', 'list': ['one', 'two', 'three']}},
              {'app': {'name': 'Me', 'my_version': '1.0', 'version': [{'major': 1, 'minor': 0}, {'major': 2, 'minor': 0}, {'major': 3, 'minor': 0}]}},
             ]

GOOD_PXY = [
"""application:
    path:
        uri_template="workitems"
        dto:
            uri="workitems/{wiid}"
            suffix=".zip"
            include: "workitems/{wiid}"
            include: "workitems/{wiid}/comments"
        collection:
            accepts="application/xml"
            schema="wi.xsd"
            uri_scheme="number"
            entry_variable="wiid"
        path:
            uri_template="workitems/{wiid}/comments"
            collection:
                accepts="application/atom+xml"
                uri_scheme="slug"
            permissions:
                add_role:
                    operations="get,head,post"
                    'Commenter'""",
"""app:
    version:
        major:
            1
        build:
            'darwin'
        minor:
            0
    name:
        'Me'
    description:
        'my thing'""",
"""{http://example.org/schemas/app}app:
    {uri:urn:oasis:version:1.0}version:
        {uri:urn:oasis:version:1.0}major:
            1
        {uri:urn:oasis:version:1.0}build:
            'darwin'
        {uri:urn:oasis:version:1.0}minor:
            0
    {http://example.org/schemas/app}name:
        'Me'
    {http://example.org/schemas/app}description:
        'my thing'""",
"""root:
    child:
        child:
            child:
                child:
                    depth = 5
    child:
        depth = 2"""]

QUALIFIED_PXY = """{http://example.org/schema/app}appRoot:
    {http://example.org/schema/app}version:
        {http://example.org/schema/app}major:
            1
        {http://example.org/schema/app}build:
            'darwin'
        {http://example.org/schema/app}minor:
            0
    {http://example.org/schema/app}name:
        'Me'
    {http://example.org/schema/app}description:
        'my thing'"""
