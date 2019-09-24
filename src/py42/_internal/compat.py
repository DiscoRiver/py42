"""
This module handles import compatibility issues between Python 2 and
Python 3.
"""
# pylint: disable=undefined-variable,import-error,unused-import,no-name-in-module

import sys

_ver = sys.version_info

try:
    import Queue as queue
except ImportError:
    import queue

#: Python 2.x?
is_py2 = (_ver[0] == 2)

if is_py2:
    from urlparse import urljoin, urlparse
    str = unicode
else:
    from urllib.parse import urljoin, urlparse
    str = str
