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

class ReportFactory:

    def __init__(self, path_reports, pdf_builder, **kargs):
        """
        pdf_builder: instance of PdfBuilder* class
        """

        self.pdf_builder = pdf_builder
        self.path_reports = path_reports
        self.__dict__.update(kargs)


    def _get_path_report(report):
        raise NotImplementedError


    def dumps(self, report):    
        """
        report: instance of ReportHtml class

        call self.pdf_builder.output(path_report, 'F') to create file pdf
        """
        raise NotImplementedError
