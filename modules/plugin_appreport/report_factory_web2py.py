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
import datetime
from libs.appreport.report_factory import ReportFactory

class ReportFactoryWeb2py(ReportFactory):

    def __init__(self, response, **kargs):
        """
        pdf_builder: instance of PdfBuilder* class
        """

        self.response = response
        ReportFactory.__init__(self, **kargs)


    def _get_path_report(self, report):
        t = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        return os.path.join(self.path_reports, 'report_%s_%s_%s.pdf'%(report.get('table', report.get('view_name','')), report.get('user_name', ''), t))


    def dumps(self, report = None):
        """
        report: instance of ReportHtml class
        """

        if not report:
          report = self.pdf_builder.report

        if not os.path.exists(self.path_reports):
            os.makedirs(self.path_reports)

        path_report = self._get_path_report(report = report)

        self.pdf_builder.output(path_report, 'F')

        file_report = open(path_report,"rb").read()

        if path_report.endswith('.pdf'):
            os.unlink(path_report)

        response_filename = report.get('response_filename', path_report)

        self.response.headers['Content-Type']='application/pdf'
        self.response.headers['Content-Disposition'] = 'attachment; filename=%s'%os.path.basename(response_filename)

        return file_report #return response.stream(path_report)
