# -*- coding: utf-8 -*- 

import sys

if request.env.web2py_runtime_gae:
    db = DAL('gae://mynamespace')
    session.connect(request, response, db = db)
elif 'java' in sys.platform:
    #TODO REPORT ERROR JDBC SQLITE AND POSTGRESX
    db = DAL('jdbc:sqlite://storage.sqlite') # or DAL('jdbc:postgres://postgres:postgres@localhost:5432/plugin_appreport')
else:
    db = DAL('sqlite://storage.sqlite') # or DAL('postgres://postgres:postgres@localhost:5432/plugin_appreport')

from gluon.tools import PluginManager, Service, Crud
plugins = PluginManager()
service = Service()
crud = Crud(db)

person = db.define_table('person',
    Field('name'),
    Field('phone'),
    Field('email'))

person.name.requires = IS_NOT_EMPTY()
person.email.requires = IS_NULL_OR(IS_EMAIL())

favorite_music = db.define_table('favorite_music',
    Field('person', person),
    Field('title'),
    Field('artist'))

favorite_music.person.requires = IS_IN_DB(db, person.id, '%(name)s')
favorite_music.title.requires = IS_NOT_EMPTY()
