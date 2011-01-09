# -*- coding: utf-8 -*-

import os.path
import sys

try:    
    from gluon.html import *
    from gluon.http import *
    from gluon.validators import *
    from gluon.sqlhtml import *
except:
    #not running on web2py
    pass

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

class Report():

    def __init__(self, user_name = 'anonymous', title = 'Report', orientation = 'P', unit = 'mm', format = 'A4'):

        self.user_name = user_name if user_name is not None and user_name.strip() != '' else 'anonymous'
        self.title = title
        self.orientation = orientation
        self.unit = unit
        self.format = format

class ReportHtml(Report):

    def __init__(self, html, user_name = 'anonymous', title = 'Report',  
        orientation = 'P', unit = 'mm', format = 'A4'):

        self.html = html
        Report.__init__(self, user_name = user_name, title = title, 
            orientation = orientation, unit = unit, format = format)

    def get_html(self):
        return self.html


class ReportHtmlDb(ReportHtml):

    def __init__(self, db, table, filter = '', user_name = 'anonymous', title = 'Report', 
        orientation = 'P', unit = 'mm', format = 'A4'):
   
        self.db = db 
        self.table = table
        self._filter = filter
        ReportHtml.__init__(self, user_name = user_name, title = title, 
            html = self.get_html(), orientation = orientation, unit = unit, format = format)

    def _get_filter(self):

        return self._filter

    def get_html(self):

        raise NotImplementedError


class ReportHtmlDbWeb2py(ReportHtmlDb):
    

    def __init__(self, table, filter = '', user_name = 'anonymous', title = 'Report', orientation = 'P', unit = 'mm', format = 'A4'):
        
        ReportHtmlDb.__init__(self, db = table._db, table = table, filter = filter, user_name = user_name,  
            title = title, orientation = orientation, unit = unit, format = format)

    def __get_name_field(self, filter):
        #caso possua '.' (no caso de tabela.field) desconsidera o valor anterior ao '.'
        return filter.split('.')[1] if filter.find('.') > -1 else filter

    def __get_type_field(self, name):
        return self.table[name].type

    def _get_filter(self):
        s = ''
        i = 0
        for f in self._filter:
            v = self._filter[f]
            
            #if value not empty
            if (isinstance(v, str) and v.strip() != '') or (not isinstance(v, str) and v is not None):
                
                #add quotes
                if self.__get_type_field(name = self.__get_name_field(filter = f)) in \
                    ('string', 'text', 'date', 'datetime'):
                    v = '"%s"'%v

                and_ = ' & ' if s.strip() != '' and len(self._filter) > 1 and i <= len(self._filter) -1 else ''
                s += '%s(self.db.%s == %s)'%(and_, f, v)
            i += 1

        if s.strip() != '':
            exec('f = %s'%s)
        else:
            #if empty set default filter
            f = self.table.id > 0
        return f

    def get_html(self):
            
        #TODO: se records < 1 então exibir mensagem sem dados para exibir ?
        records = self.db(self._get_filter()).select()
        return '<html>%s</html>'%BODY(SQLTABLE(records, headers='fieldname:capitalize'))
