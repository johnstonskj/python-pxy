""" 
The setup/config script for the pxy package.

Licensed Materials - Property of IBM
Copyright IBM Corp. 2007.  All Rights Reserved.

US Government Users Restricted Rights - Use, duplication or disclosure
restricted by GSA ADP Schedule Contract with IBM Corp.
"""

#import ez_setup
#ez_setup.use_setuptools()

from setuptools import setup, find_packages

import pxy

setup(name=pxy.__name__,
      version=pxy.__version__,
      description='Parser/writer for the PXY compact XML form.',
      author=pxy.__author__,
      author_email=pxy.__author_email__,
      url='http://www.ibm.com/developerworks/blog/pages/johnston',
      packages=find_packages(exclude=['test']),
      entry_points = {
        'console_scripts': [
            'pxy2xml = pxy.script:pxy_to_xml',
            'xml2pxy = pxy.script:xml_to_pxy',
        ], 
      },
      test_suite = 'test.alltests'
     )
