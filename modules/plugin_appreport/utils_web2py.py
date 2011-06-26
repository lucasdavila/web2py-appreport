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

class UtilsWeb2py:

    def __get_name_field(self, filter):
        #caso possua '.' (no caso de tabela.field) desconsidera o valor anterior ao '.'
        return filter.split('.')[1] if filter.find('.') > -1 else filter

    def __get_type_field(self, name, table):
        return table[name].type

    def prep_filter(self, table, vars = {}):
        """ Prepara um filtro (where) para seleção no banco de dados, conforme vars de um form.

            Exemplo form com campo Id e valor 1,
            prepara o filtro <table>.id == 1

            vars: dict(form.vars)
            table: db.mytaable
        

        """
        db = table._db
        s = ''
        i = 0
        for f in vars:
            v = vars[f]
            
            #if value not empty
            if (isinstance(v, str) and v.strip() != '') or (not isinstance(v, str) and v is not None):
                
                #add quotes
                if self.__get_type_field(name = self.__get_name_field(filter = f), table = table) in \
                    ('string', 'text', 'date', 'datetime'):
                    v = '"%s"'%v

                and_ = ' & ' if s.strip() != '' and len(vars) > 1 and i <= len(vars) -1 else ''
                s += '%s(db.%s == %s)'%(and_, f, v)
            i += 1

        if s.strip() != '':
            exec('f = %s'%s)
        else:
            #if empty set default filter
            f = table.id > 0
        return f
