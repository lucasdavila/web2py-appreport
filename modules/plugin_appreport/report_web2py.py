# coding: utf8

from gluon.html import *
from gluon.http import *
from gluon.validators import *
from gluon.sqlhtml import *

import utils_web2py
from libs.appreport.report import ReportHtmlDb

class ReportHtmlDbWeb2py(ReportHtmlDb):

    def __init__(self, table, **kargs):
        ReportHtmlDb.__init__(self, db = table._db, table = table, **kargs)


    def _get_args(self):
        return utils_web2py.UtilsWeb2py().prep_filter(vars = self.get('args', {}), table = self.get('table'))


    def get_html(self):
        #TODO: se records < 1 então exibir mensagem sem dados para exibir ?
        records = self.db(self._get_args()).select()
        return '<html><head><meta charset="%s" /></head>%s</html>'%(self.get('charset', 'utf-8'), BODY(H2(self.get('title', 'Report')),SQLTABLE(records, headers='fieldname:capitalize')))


