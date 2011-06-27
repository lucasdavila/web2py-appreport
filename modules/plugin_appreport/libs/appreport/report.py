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

import os.path
import sys

class Report():

    def __init__(self, **kargs):
        self.user_name = kargs.get('user_name') or 'anonymous'
        self.__dict__.update(kargs)

    
    def get(self, att_name, default_value = None):
      return self.__dict__.get(att_name, default_value)


class ReportHtml(Report):

    def __init__(self, **kargs):

        self.html = kargs.get('html', '')
        Report.__init__(self, **kargs)


    def get_html(self):
        return self.html


class ReportHtmlDb(ReportHtml):

    def __init__(self, db, table, **kargs):
        
        self.db = db 
        self.table = table
        self.args = kargs.get('args', kargs.get('filter', ''))
        ReportHtml.__init__(self, **kargs)
        self.html = self.get_html()

    def _get_args(self):
        return self.args


    def get_html(self):
        raise NotImplementedError
