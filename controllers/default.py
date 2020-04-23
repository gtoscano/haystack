# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# ---- example index page ----
def index():
    response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))

# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki() 

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)
    

def testing_haystack():
    from haystack import Haystack
    index = Haystack(db.thing, core="things")
    index.indexes('name','description')

    # Following the test example in mdipierro's plugin

    # Let's insert two things
    db.thing.insert(name="table",description = "one table")
    id = db.thing.insert(name="table",description = "another table")

    #there should be one description with a 'one' word
    print (db(index.search(description='one')).count())
    #there should be two descriptions with a 'table' word
    print ( db(index.search(description='table')).count())

    # more experiments
    print ( db(index.search(name='table')).count() )
    print ( db(index.search(name='table',description='table')).count() )

    # let's change the last inserted thing
    db(db.thing.id==id).update(name='table',description='four legs')


    # some queries
    print ( db(index.search(description='another')).count() )
    print ( db(index.search(description='four')).count() )
    print ( db(index.search(description='legs')).count() )
    print ( db(index.search(description='legs four')).count() )
    print ( db(index.search(name='table')).count() )
    print ( db(index.search(name='table',description='table')).count() )
    print ( db(index.search(name='table')|
              index.search(description='table')).count() )

    # Lets delete the latest entry
    db(db.thing.id==id).delete()

    # check that i has been deleted
    print ( db(index.search(name='table')).count())
    
    # update of the remaining entry
    row  = db(db.thing.id > 0 ).select().first()
    row.update_record(name='table2', description='third table')

    # one more insert
    db.thing.insert(name="table",description = "forth table")

    rows = db(index.search(name = 'table',description='table', mode='OR')).select()
    
    for row in rows:
        print(row)

    return dict(title = 'Testing completed')

def indexing_already_stored_info():
    from haystack import Haystack

    #inserting before tracking changes
    db.thing.insert(name="table",description = "seventh table")
    db.thing.insert(name="table2",description = "eightth table")
    db.thing.insert(name="table2",description = "nineth table")


    index = Haystack(db.thing, core="things") #be shure to create things in solr bin/solr create -c things
    index.indexes('name','description')

    # index all entries
    index.index_table((db.thing.id > 0) , db)
    
    return dict(title = 'Table things was succesfuly indexed')



def my_search():
    from haystack import Haystack

    search_string = request.args(0)
    
    if search_string == None:
        search_string = ''
    else:
        search_string = search_string.replace('_', ' ')

    if 'inputsearch' in request.vars.keys():
        search_string = request.vars['inputsearch']

    
    things = []
    if search_string != '':
        index = Haystack(db.thing, core="things")
        index.indexes('name','description')
    
        rows = db(index.search(name = search_string, description = search_string, mode='OR')).select()
        
    
        for row in rows:
            things.append({'id':row.id, 'name':row.name, 'description':row.description})
    
    return dict(things = things)


