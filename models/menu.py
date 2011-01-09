# -*- coding: utf-8 -*- 

response.title = 'Plugin appreport'
response.subtitle = T('customize me!')

#http://dev.w3.org/html5/markup/meta.name.html 
response.meta.author = 'you'
response.meta.description = 'Free and open source full-stack enterprise framework for agile development of fast, scalable, secure and portable database-driven web-based applications. Written and programmable in Python'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Enterprise Framework'
response.meta.copyright = 'Copyright 2007-2010'


response.menu = [
    (T('Home'), False, URL(request.application,'default','index'), [])
    ]

response.menu+=[
    (T('Files'), False, URL(request.application,'default','index'), [
    ('person', False, URL(r=request, c='person', f='create')),])
    ]

response.menu+=[
    (T('Repors'), False, URL(request.application,'default','index'), [
    ('person', False, URL(r=request, c='person', f='report')),
    ('Custon report', False, URL(r=request, c='person', f='custom_report')),    
    ])
    ]

response.menu += [
    (T('About'), False, URL(request.application,'default','about'), [])
    ]
