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

from libs import utils

try:    
    from gluon.html import *
    from gluon.http import *
    from gluon.validators import *
    from gluon.sqlhtml import *
except:
    #not running on web2py
    pass

class Report():

    def __init__(self, user_name = 'anonymous', title = 'Report', orientation = 'P', unit = 'mm', format = 'A4'):
        """ Orientation: 'P' for portrait (retrato) or 'L' for landscape (paisagem)
        """
        self.user_name = user_name if user_name is not None and user_name.strip() != '' else 'anonymous'
        self.title = title
        self.orientation = orientation
        self.unit = unit
        self.format = format


class ReportHtml(Report):

    def __init__(self, html, user_name = 'anonymous', title = 'Report',  
        orientation = 'P', unit = 'mm', format = 'A4', charset = 'utf-8'):

        self.html = html
        self.charset = charset
        Report.__init__(self, user_name = user_name, title = title, 
            orientation = orientation, unit = unit, format = format)

    def get_html(self):
        return self.html


class ReportHtmlDb(ReportHtml):

    def __init__(self, db, table, filter = '', user_name = 'anonymous', title = 'Report', 
        orientation = 'P', unit = 'mm', format = 'A4', charset = 'utf-8'):
        
        self.db = db 
        self.table = table
        self._filter = filter
        ReportHtml.__init__(self, user_name = user_name, title = title, html = '', orientation = orientation, unit = unit, format = format, charset = charset)
        self.html = self.get_html()

    def _get_filter(self):

        return self._filter

    def get_html(self):

        raise NotImplementedError


class ReportHtmlDbWeb2py(ReportHtmlDb):
    

    def __init__(self, table, filter = '', user_name = 'anonymous', title = 'Report', orientation = 'P', unit = 'mm', format = 'A4', charset = 'utf-8'):

        ReportHtmlDb.__init__(self, db = table._db, table = table, filter = filter, user_name = user_name,  
            title = title, orientation = orientation, unit = unit, format = format, charset = charset)


    def _get_filter(self):

        return utils.UtilsWeb2py().prep_filter(vars = self._filter, table = self.table)

    def get_html(self):
            
        #TODO: se records < 1 então exibir mensagem sem dados para exibir ?
        records = self.db(self._get_filter()).select()
        return '<html><head><meta charset="%s" /></head>%s</html>'%(self.charset, BODY(H2(self.title),SQLTABLE(records, headers='fieldname:capitalize')))
