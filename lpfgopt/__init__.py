#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
mypackage_root_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(mypackage_root_dir, 'VERSION.txt')) as version_file:
    __version__ = version_file.read().strip()
del os
