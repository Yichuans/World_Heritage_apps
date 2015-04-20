# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Welcome to web2py!")
    return dict(message=T('Hello World'))


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())

## FUNCTIONS ========================
def mkd_file_exists(wdpaid):
    import os
    mkdfile = os.path.join(request.folder, 'mydata', str(wdpaid) + '.md')

    if os.path.exists(mkdfile):
        return True

    return False


def get_wh_mkd(wdpaid):
    """get wh datasheet in mkd by id"""
    import os
    try:
        with open(os.path.join(request.folder, 'mydata', str(wdpaid) + '.md'), 'r') as f:
            content = f.read()
        return content
    except:
        return ''

def get_last_updated(wdpaid):
    """get information about wh datasheet by id"""
    import os, time
    wh_path = os.path.join(request.folder, 'mydata', str(wdpaid) + '.md')
    wh_stat = os.stat(wh_path)
    return 'Last uploaded on: ' + time.ctime(wh_stat.st_mtime)

def render_wh_mkd_to_html(wh_mkd):
    """render wh markdown file to html"""
    import gluon.contrib.markdown.markdown2 as md
    mymd = md.Markdown()
    wh_html = mymd.convert(wh_mkd)
    return wh_html

def write_wh_mkd(wdpaid, wh_mkd):
    """write update to wh datasheet in mkd by id, to be used in combination with GIT to track changes"""
    import os
    try:
        with open(os.path.join(request.folder, 'mydata', str(wdpaid) + '.md'), 'w') as f:
            f.write(wh_mkd)
        return True
    except:
        return False

def bs_wh_html_add_h2_id(wh_html):
    """use BeautifulSoup to create ID for each heading using safe strings
    return 
    modified HTML
    """
    # NEED TO INSTALL BS IN THE DEPLOYMENT ENVINRONMENT
    from bs4 import BeautifulSoup as bs

    # find all h2
    soup = bs(wh_html)
    h2_list = soup('h2')

    for each_h2 in h2_list:
        # get the valid name for id
        new_string = slugify(''.join(each_h2.strings))
        each_h2['id'] = new_string

        # replace the name as well
        each_h2.string = render_h2_beautify(each_h2)

    return soup.prettify()

def render_h2_beautify(bs_h2):
    newstring = ''.join(bs_h2.strings).lower().title()
    if 'And' in newstring:
        newstring = newstring.replace('And', 'and')
    if 'Of' in newstring:
        newstring = newstring.replace('Of', 'of')        
    if 'Iucn' in newstring:
        newstring = newstring.replace('Iucn', 'IUCN')
       
    return newstring


def bs_wh_html_h2_anchor(wh_html):
    """use BeautifulSoup to create anchor for each heading using safe strings
    return 
    list of anchors
    """
    # NEED TO INSTALL BS IN THE DEPLOYMENT ENVINRONMENT
    from bs4 import BeautifulSoup as bs

    # find all h2
    soup = bs(wh_html)
    h2_list = soup('h2')

    # dictionary
    anchor_tuples = list()

    for each_h2 in h2_list:
        # get the valid name and keep 'and' lowercase and 'IUCN' upper
        anchor_name = render_h2_beautify(each_h2)

        # create anchor    
        anchor = slugify(''.join(each_h2.strings))
        anchor_tuples.append((anchor, anchor_name))

    return anchor_tuples

def slugify(value):
    """
    Django utility
    Converts to ASCII. Converts spaces to hyphens. Removes characters that
    aren't alphanumerics, underscores, or hyphens. Converts to lowercase.
    Also strips leading and trailing whitespace.
    """
    import re, unicodedata
    if type(value) != str:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub('[^\w\s-]', '', value).strip().lower()
    value = value.replace(' ', '-')
    return value

# def test():
#     wdpaid = 191
#     wh_html = render_wh_mkd_to_html(get_wh_mkd(wdpaid))
#     return bs_wh_html_add_h2_id(wh_html)
#     # return bs_wh_html(wh_html)    


## CONTROLLER ====================== 
def ajax_wh_mkd_to_html():
    """ Ajax call to return updated mkd"""
    return render_wh_mkd_to_html(request.post_vars['mkd'])

def wh_html():
    # show page
    wdpaid = request.args[0]

    # get anchor navi
    anchor_tuples = bs_wh_html_h2_anchor(render_wh_mkd_to_html(get_wh_mkd(wdpaid)))

    div_navi = DIV(_id = 'doc_navi')
    # header
    p = H3('Table of Content:', _id='toc')
    div_navi.append(p)

    # toc
    ul = UL(_class = 'nav nav-pills nav-stacked', _role="tablist")

    for anchor, anchor_name in anchor_tuples:
        # add each anchor element
        ul.append(LI(A(anchor_name, _class = 'adjusted_anchor', _href = URL('wh_html', args=[wdpaid,]) + '#' + str(anchor))))

    div_navi.append(ul)

    # main html
    content_html = bs_wh_html_add_h2_id(render_wh_mkd_to_html(get_wh_mkd(wdpaid)))

    div_content = DIV(_id = 'doc_content')
    div_content.append(XML(content_html))

    # last update text
    lastupdate_text = get_last_updated(wdpaid)

    return dict(mycontent = div_content, mynavi = div_navi, lastupdate = lastupdate_text)

def wh_html_bs():
    # show page bootstrap CSS
    wdpaid = request.args[0]

    # get anchor navi
    anchor_tuples = bs_wh_html_h2_anchor(render_wh_mkd_to_html(get_wh_mkd(wdpaid)))

    div_navi = DIV(_class="col-xs-6 col-sm-3 sidebar-offcanvas", _id="sidebar", _role="navigation")

    # header
    p = H3('Table of Content:', _id='toc')
    div_navi.append(p)

    # toc
    ul = UL(_class='nav')

    for anchor, anchor_name in anchor_tuples:
        # add each anchor element
        ul.append(LI(A(anchor_name, _href = URL('wh_html_bs', args=[wdpaid,]) + '#' + str(anchor))))

    div_navi.append(ul)

    # main html
    content_html = bs_wh_html_add_h2_id(render_wh_mkd_to_html(get_wh_mkd(wdpaid)))

    div_content = DIV(_class ='col-xs-12 col-sm-9')
    div_content.append(XML(content_html))

    # last update text
    lastupdate_text = get_last_updated(wdpaid)

    return dict(mycontent = div_content, mynavi = div_navi, lastupdate = lastupdate_text)

def wh_html_bs2():
    # show page bootstrap CSS
    wdpaid = request.args[0]

    wh_name = db(db.wh.wdpaid==wdpaid).select()[0].name

    if not mkd_file_exists(wdpaid):
        raise HTTP(400, 'The page doesn\'t exists or has been removed')

    # get anchor navi ===========
    anchor_tuples = bs_wh_html_h2_anchor(render_wh_mkd_to_html(get_wh_mkd(wdpaid)))
    div_navi = list()

    for anchor, anchor_name in anchor_tuples:
        # add each anchor element
        div_navi.append(LI(A(anchor_name, _href = '#' + str(anchor))))

    # main html ============
    content_html = bs_wh_html_add_h2_id(render_wh_mkd_to_html(get_wh_mkd(wdpaid)))
    div_content = DIV()
    div_content.append(XML(content_html))

    # last update text ============
    lastupdate_text = get_last_updated(wdpaid)

    return dict(wh_name=wh_name, mycontent = div_content, mynavi = div_navi, lastupdate = lastupdate_text)

def wh_html_bs2_edit():
    # edit page
    wdpaid = request.args[0] # test 191

    if not mkd_file_exists(wdpaid):
        raise HTTP(400, 'The page doesn\'t exists or has been removed')

    # create a form to accept updates
    form = SQLFORM.factory(
    Field('markdown', 'text', length=9999999999))

    # prepopulate data from text file
    form.vars.markdown = get_wh_mkd(wdpaid)

    # update the record
    if form.process(keepvalues=True).accepted:
        if write_wh_mkd(wdpaid, request.post_vars.markdown):
            response.flash = 'form accepted and record updated'
        else:
            response.flash = 'Error: not updated!'

    # preview
    preview = DIV()
    preview.append(XML(render_wh_mkd_to_html(get_wh_mkd(wdpaid))))

    return dict(form=form, preview=preview)

def edit_wh_html():
    # edit page
    wdpaid = request.args[0] # test 191

    # create a form to accept updates
    form = SQLFORM.factory(
    Field('wdpaid', 'string',),
    Field('markdown', 'text', length=9999999999))

    # prepopulate data from text file
    form.vars.wdpaid = wdpaid
    form.vars.markdown = get_wh_mkd(wdpaid)

    # update the record
    if form.process(keepvalues=True).accepted:
        if write_wh_mkd(wdpaid, request.post_vars.markdown):
            response.flash = 'form accepted and record updated'
        else:
            response.flash = 'Error: not updated!'

    return dict(form=form)



# ============== test
def _test_():
    wdpaid = 191
    return bs_wh_html_h2_anchor(render_wh_mkd_to_html(get_wh_mkd(wdpaid)))

def hello():
    return dict()

def test_last_updated():
    wdpaid = request.args[0]
    return get_last_updated(wdpaid)

def test_view():
    wdpaid = request.args[0]
    return bs_wh_html_add_h2_id(render_wh_mkd_to_html(get_wh_mkd(wdpaid)))

