# -*- coding: utf-8 -*-

"""
Copyright (c) 2010, 2011 Lucas D'Avila - email lucassdvl@gmail.com / twitter @lucadavila

This file is part of appreport.

appreport is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License (LGPL v3) as published by
the Free Software Foundation, on version 3 of the License.

appreport is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with appreport.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys

if 'java' in sys.platform.lower():
    import os, glob
    jars = glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), "jasper/*.jar"))
    for jar in jars:
      if jar not in sys.path:
        sys.path.append(jar)
        #print 'added jar: %s'%jar
