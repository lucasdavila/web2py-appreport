# coding: utf8

#to start using plugin_appreport in a controller define the following action:   
#para começar a usar o plugin_appreport em um controlador defina o seguinte action:
#
#def report():
#    form = plugin_appreport.REPORTFORM(db.table_name)
#    
#    if form.accepts(request.vars, session):
#        return plugin_appreport.REPORT(table = db.table_name, title = 'List of ?',filter = dict(form.vars))
#            
#    return dict(form = form)


#reference to appreport module
plugin_appreport_appreport = local_import('plugin_appreport.appreport', reload = False)

class PluginAppreport:
    
    def REPORTFORM(self, table):
        """wrapper to module >> appreport.form_report_web2py / class >> FormReportWeb2py / method >> get_form
        """
        dir(plugin_appreport_appreport)
        return plugin_appreport_appreport.form_report.FormReportWeb2py(table = table).get_form()

    #TODO add parametro html, se != None chamar classe html ?
    def REPORT(self, table = None, filter = '', title = 'Report', html = '', orientation = 'P', unit = 'mm', format = 'A4'):
        """wrapper to module >> appreport.report_html_db_web2py / class >> ReportHtmlDbWeb2py / method >> dumps

        table = db.table    
        filter = dict(form.vars) or {'table_name.field_name':'value', 'table_name.field2_name':'value2'}
        title = 'title of report'
        html = html custom if given the report will be generated as html passed, ignoring the table definition, example:
            <html>
                <body>
                    <table>
                        <thead>
                            <tr>
                                <th>Id</th>
                                <th>Name</th>
                                <th>Phone</th>
                                <th>Email</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>1</td>
                                <td>lucas davila</td>
                                <td>123455</td>
                                <td>lucassdvl@gmail.com</td>
                            </tr>
                        </tbody>
                    </table>
                </body>
            </html>

            
        Orientation: 'P' for portrait (retrato) or 'L' for landscape (paisagem)
    
        """
        
        user_name = auth.user.first_name if auth.user is not None else ''
        
        if html.strip() != '':
            report = plugin_appreport_appreport.report.ReportHtml(user_name = user_name,
            title = title, html = html, orientation = orientation, unit = unit, format = format)
        else:
            report = plugin_appreport_appreport.report.ReportHtmlDbWeb2py(table = table, filter = filter, user_name = user_name, title = title, orientation = orientation, unit = unit, format = format)
                    
        pdf_builder = plugin_appreport_appreport.pdf_builder.PdfBuilderPyfpdf(report = report)
            
        return plugin_appreport_appreport.report_factory.ReportFactoryWeb2py(response = response, request = request, path_reports = 'private/plugin_appreport/reports', pdf_builder = pdf_builder).dumps(report = report)
            
plugin_appreport = PluginAppreport()
