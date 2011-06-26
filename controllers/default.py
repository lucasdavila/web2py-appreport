# -*- coding: utf-8 -*- 
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

def index():
    return dict()


def about():
    return {}


def user():
    """
    exposes:
    http://..../[app]/default/user/login 
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    session.forget()
    return service()


def report():
    session.forget()
    return service()

import xmlrpclib

@service.xmlrpc
def pdf(view_name, username = '', args = {}, *_args, **kargs):

    if not view_name:
        raise Exception('Invalid view_name')
    if not isinstance(view_name, str):
        raise Exception('View_name must be string')
    if not isinstance(username, str):
        raise Exception('Username must be string')
    elif not isinstance(args, dict):
        raise Exception('Invalid args')

    report = xmlrpclib.Binary(plugin_appreport.REPORTJASPER(view_name = view_name, args = args))

    return dict(report_name = '%s_%s.pdf'%(view_name, username), report = report)
