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

class ReportFactory:

    def __init__(self, path_reports, pdf_builder):
        """
        pdf_builder: instance of PdfBuilder* class
        """

        self.pdf_builder = pdf_builder
        self.path_reports = path_reports

    def _get_path_report(report):
    
        raise NotImplementedError

    def dumps(self, report):    
        """
        report: instance of ReportHtml class

        call self.pdf_builder.output(path_report, 'F') to create file pdf
        """
    
        raise NotImplementedError


class ReportFactoryWeb2py(ReportFactory):
    
    def __init__(self, response, request, path_reports, pdf_builder):
        """
        pdf_builder: instance of PdfBuilder* class
        """

        self.response = response
        self.request = request
        ReportFactory.__init__(self, path_reports = path_reports, pdf_builder = pdf_builder)

    def _get_path_report(self, report):
        t = ('%s'%self.request.now).replace(' ', '_').replace(':', '-').replace('.', '_')

        table_name = '%s_'%report.table._tablename if hasattr(report, 'table') else ''
        return os.path.join(self.path_reports, 'report_%s%s_%s.pdf'%(table_name, report.user_name, t))

    def dumps(self, report):    
        """
        report: instance of ReportHtml class
        """

        if not os.path.exists(self.path_reports): os.makedirs(self.path_reports)                            
        path_report = self._get_path_report(report = report)

        self.pdf_builder.output(path_report, 'F')      

        file_report = open(path_report,"rb").read()
        if path_report.endswith('.pdf'):
            os.unlink(path_report)
        self.response.headers['Content-Type']='application/pdf'
        disposition = 'attachment; filename=%s'%os.path.basename(path_report)
        self.response.headers['Content-Disposition'] = disposition
        return file_report #return response.stream(path_report)
