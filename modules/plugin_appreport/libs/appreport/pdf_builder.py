# -*- coding: utf-8 -*-

from libs.pyfpdf.fpdf import FPDF
from libs.pyfpdf.html import HTMLMixin

#FIXME report bug on jython
import sys
if 'java' not in sys.platform:
  from libs.pisa.xhtml2pdf.ho import pisa

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

#implementation to PyFpdf builder
class PdfBuilderPyfpdf(FPDF, HTMLMixin):

    def __init__(self, report):
        """
        report: instance of ReportHtml class
        """
        self.report = report

        FPDF.__init__(self, orientation = self.report.get('orientation', 'P'), unit = self.report.get('unit', 'mm'), 
            format = self.report.get('format', 'A4'))

        self.set_title(title = self.report.get('title', ''))

        #TODO verificar porque da necessidade da chamada ao metódo abaixo, refatorar ?
        #First page
        self.add_page()

        self.write_html(self.report.get_html())

    def header(self):
        #self.image('tutorial/logo_pb.png',10,8,33)
        self.set_font('Arial','B',15)
        self.cell(80)
        #TODO remover borda titulo
        #self.cell(30,10, self.title,1,0,'C')
        self.cell(w = len(self.report.get('title', '')), txt = self.report.get('title', ''), align = 'C')
        self.ln(5)
            
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial','I',8)
        txt = '%s / %s' % (self.page_no(), self.alias_nb_pages())
        self.cell(0,10,txt,0,0,'R')


#implementation to Pisa builder
class PdfBuilderPisa:

    def __init__(self, report = None):
        """
        report: instance of ReportHtml class
        """

        self.report = report


    def output(self, path_report, *args, **kargs):

        doc = file(path_report, "wb")
        pdf = pisa.CreatePDF(self.report.get_html(), dest = doc)
        doc.close()

        if kargs.get('print_errors') and pdf.err:
            print "Errors on output report: %"%pdf.err
