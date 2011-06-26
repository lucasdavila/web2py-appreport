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

from gluon.html import *
from gluon.http import *
from gluon.validators import *
from gluon.sqlhtml import *
import utils_web2py

#TODO overwrite class FORM() ?
class FormReportWeb2py():
    
    def __init__(self, table, ignore_r = False):

        self.table = table
        self.ignore_r = ignore_r

    def _get_default_validation(self, field_type):

        default_validations = (dict(field_type = 'date', validation = IS_EMPTY_OR(IS_DATE())),
                               dict(field_type = 'time', validation = IS_EMPTY_OR(IS_TIME())),
                               dict(field_type = 'datetime', validation = IS_EMPTY_OR(IS_DATETIME())),
                              )
        return [v['validation'] for v in default_validations if v['field_type'] == field_type]

    def get_form(self):

        fields = [f.name for f in self.table if (self.ignore_r or f.readable)]
        form = FORM(TABLE(), INPUT(_type = 'submit', _value = 'Exibir'))

        list_fields = []
        for field_name in fields:
            field = self.table[field_name]

#            list_fields.append([LABEL('%s:'%field.label), XML(SQLFORM.widgets.integer.widget(field, ''))])
            list_fields.append([LABEL('%s:'%field.label), SQLFORM.widgets.string.widget(field, '', 
            _name = '%s.%s'%(self.table._tablename, field_name), requires = self._get_default_validation(field.type))])
            
        for f in list_fields:
            #insert rows in table
            form[0].append(TR(
                TD(f[0]),
                TD(f[1])
                ))

            form.prep_filter = self.prep_filter

        return form

    def prep_filter(self, filter):

        """

        Example use:
        
            #in a controller define the following action:
            def complex_report():
                form = FormReportWeb2py(table=person)

                if form.accepts(request.vars, session):
                    persons = db(form.prep_filter(filter = dict(form.vars))).select()
                    html = response.render('person/report_persons.html', dict(persons = persons))
                    return ReportHtml(html = html)

                return dict(form = form)
        """

        return utils_web2py.UtilsWeb2py().prep_filter(vars = filter, table = self.table)
