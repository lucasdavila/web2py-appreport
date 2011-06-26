# coding: utf8

def create():

    form = crud.create(person)
    form_favs = crud.create(favorite_music)
    persons = db().select(db.person.ALL, db.favorite_music.ALL, left=favorite_music.on(person.id == favorite_music.person))

    return dict(form = form, form_favs = form_favs, persons = persons)
    

def simple_report():
    #generates a html form to filter the data to be displayed in the report
    form = plugin_appreport.REPORTFORM(table=person)

    if form.accepts(request.vars, session):
        #build a report based on table fields (aka auto generates html) and filters informed in form
        return plugin_appreport.REPORTPISA(table = person, title = 'List of persons', args = dict(form.vars))

    return dict(form = form)

    
def report_persons():
    return dict(persons = db(person.id > 0).select())


def complex_report():
    #generates a html form to filter the data to be displayed in the report
    form = plugin_appreport.REPORTFORM(table=person)

    if form.accepts(request.vars, session):

        #select a set of persons based on informed filters
        persons = db(form.prep_filter(filter = dict(form.vars))).select()

        #build a report based on dynamic html of view 'person/report_persons.html'
        html = response.render('person/report_persons.html', dict(persons = persons))
        return plugin_appreport.REPORTPISA(html = html)

    return dict(form = form)



def custom_report():
    
    html = """<html>
                <head>
                    <meta charset="utf-8" />
                </head>
                <body>
                    <h2>my custom report using the plugin_appreport</h2>
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
                                <td>Lucas D'Avila</td>
                                <td>lucassdvl@gmail.com</td>
                                <td>@lucadavila</td>                                
                            </tr>
                        </tbody>
                    </table>
                </body>
            </html>
    """
    #build a report based on static html
    return plugin_appreport.REPORTPISA(html = html)
    #or return plugin_appreport.REPORTPYFPDF(html = html, title = 'my custom report using the plugin appreport')
