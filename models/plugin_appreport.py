# coding: utf8

import sys
import os.path

if request.folder not in sys.path:
    sys.path.append(request.folder)

#to start using plugin_appreport in a controller define the following action:
#def custom_report():
#   return plugin_appreport.REPORTPISA(html = 'your html and css')
#
#def report():
#    #generates a html form to filter the data to be displayed in the report
#    form = plugin_appreport.REPORTFORM(db.table_name)
#    
#    if form.accepts(request.vars, session):
#        #build a report based on table fields (aka auto generates html) and filters informed in form
#        return plugin_appreport.REPORTPISA(table = db.table_name, filter = dict(form.vars))
#            
#    return dict(form = form)
#
#   more info check the project wiki on github https://github.com/lucasdavila/web2py-appreport/wiki

import modules.plugin_appreport as plugin_appreport_module

class PluginAppreport:
    
    _path_reports = os.path.join(request.folder, 'private/plugin_appreport/reports')

    def REPORTFORM(self, table):
        return plugin_appreport_module.form_report_web2py.FormReportWeb2py(table = table).get_form()


    def REPORT(self, engine = 'pyfpdf', **kargs):

        if engine == 'pisa':
            return REPORTPISA(**kargs)
        elif engine == 'pyfpdf':
            return REPORTPYFPDF(**kargs)
        else:
            raise NotImplementedError("Invalid engine: '%s', try use 'pisa' or 'pyfpdf'"%engine)


    def _fix_kargs(self, kargs):   
        if not kargs.get('user_name'):
            kargs.update({'user_name' : auth.user.first_name if 'auth' in globals() and auth.user is not None else ''})     
        return kargs
            

    def __build_report(self, path_reports, pdf_builder):
        return plugin_appreport_module.report_factory_web2py.ReportFactoryWeb2py(response = response, request = request, path_reports = path_reports, pdf_builder = pdf_builder).dumps()   


    def REPORTPISA(self, table = None, filter = {}, html = '', **kargs):
        """

        You can pass the html manually *or* pass a table and a filter to automatically generate the html (based on table field and filtered using the filter :P )

        Expected argument:
            - filter (or args): dict(form.vars) or {'table_name.field_name':'value', 'table_name.field2_name':'value2'}
            - table: db.your_table
            - html: string containing html and css

        Note:
            -if you pass the html (aka != '') the report will be generated manually using html *ignoring* the table and filter

        """
        kargs = self._fix_kargs(kargs)

        if html.strip() != '':
            report = plugin_appreport_module.libs.appreport.report.ReportHtml(html = html, **kargs)
        else:
            report = plugin_appreport_module.report_web2py.ReportHtmlDbWeb2py(table = table, filter = filter, **kargs)        

        pdf_builder = plugin_appreport_module.libs.appreport.pdf_builder.PdfBuilderPisa(report = report)
        return self.__build_report(self._path_reports, pdf_builder)


    def REPORTPYFPDF(self, table = None, filter = {}, html = '', charset = 'utf-8', title = 'Report', orientation = 'P', unit = 'mm', format = 'A4', **kargs):
        """
        Expected arguments:
            - filter (or args): dict(form.vars) or {'table_name.field_name':'value', 'table_name.field2_name':'value2'}
            - table: db.your_table
            - html: string containing html

        You can pass the html manually *or* pass a table and a filter to automatically generate the html (based on table field and filtered using the filter :P )

        Notes:
            - if you pass the html (aka != '') the report will be generated manually using html *ignoring* the table and filters
            - css are not supported in pyfpdf, to customize the report, see the arguments explanation below

        Other arguments supported by pyfpdf:
            - charset = 'utf-8' 
            - title = 'title of report' 
            - orientation = 'P' (for portrait (retrato)) or ('L' for landscape (paisagem)) 
            - unit = 'mm' 
            - format = 'A4'

        """
        kargs = self._fix_kargs(kargs)


        if html.strip() != '':
            report = plugin_appreport_module.libs.appreport.report.ReportHtml(html = html, charset = charset, title = title, orientation = orientation, unit = unit, format = format, **kargs)
        else:
            report = plugin_appreport_module.report_web2py.ReportHtmlDbWeb2py(table = table, filter = filter, charset = charset, title = title, orientation = orientation, unit = unit, format = format, **kargs)

        pdf_builder = plugin_appreport_module.libs.appreport.pdf_builder.PdfBuilderPyfpdf(report = self._get_report_instance(kargs))
        return self.__build_report(self._path_reports, pdf_builder)
     
            
plugin_appreport = PluginAppreport()
