# coding: utf8

def create():

    form = crud.create(person)
    persons = crud.select(person, person.id > 0)

    return dict(form = form, persons = persons)
    
def report():

    form = plugin_appreport.REPORTFORM(person)

    if form.accepts(request.vars, session):
        return plugin_appreport.REPORT(table = person, title = 'List of persons', filter = dict(form.vars))

    return dict(form = form)
    
def custom_report():
    
    html = """<html>
                <body>
                    <table>
                        <thead>
                            <tr>
                                <th>Author</th>
                                <th>Email</th>
                                <th>Twitter</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>Lucas Davila</td>
                                <td>lucassdvl@gmail.com</td>
                                <td>@lucadavila</td>                                
                            </tr>
                        </tbody>
                    </table>
                </body>
            </html>
    """
    return plugin_appreport.REPORT(html = html, title = 'my custom report using the plugin appreport')
