# for landcover visualisation

# ========== controller
def index():
    result = db().select(db.wh.name, db.wh.wdpaid, orderby=db.wh.name)

    li = list()
    for each in result:
        li.append(LI(A(each.name, _href = URL('site', args = [str(each.wdpaid)]), _target="_blank")))

    return dict(li=li)


def get_landcover():
    """to be call with .csv to return csv
    see views landcover/get_landcover_csv.csv
    """
    wdpaid = request.args[0]
    landcover = db(db.landcover.wdpaid==wdpaid).select(db.landcover.lc_2000, db.landcover.lc_2010, db.landcover.areakm2)


    return dict(landcover=landcover)



def conv_matrix():
    wdpaid = request.args[0]
    query = db(db.wh.wdpaid==wdpaid).select()

    if len(query) == 0:
        raise HTTP(400, 'The wdpaid doesn\'t exists, invalid or has been removed')

    wh_name = query[0].name
    return dict(wh_name=wh_name, wdpaid=wdpaid)


def map():
    wdpaid = request.args[0]

    query = db(db.wh.wdpaid==wdpaid).select()
    geo_json = db(db.wh_geom.wdpaid==wdpaid).select()

    if len(query) == 0:
        raise HTTP(400, 'The wdpaid doesn\'t exists, invalid or has been removed')

    if len(geo_json) == 0:
        raise HTTP(400, 'The wdpaid doesn\'t have a map')


    wh_name = query[0].name
    wh_geo_json = geo_json[0].geo_json

    return dict(wh_name=wh_name, wh_geo_json=wh_geo_json)

# ========= individual page
def site():
    wdpaid = request.args[0]

    query = db(db.wh.wdpaid==wdpaid).select()
    geo_json = db(db.wh_geom.wdpaid==wdpaid).select()

    if len(query) == 0:
        raise HTTP(400, 'The wdpaid doesn\'t exists, invalid or has been removed')

    if len(geo_json) == 0:
        raise HTTP(400, 'The wdpaid doesn\'t have a map')


    wh_name = query[0].name
    wh_geo_json = geo_json[0].geo_json

    return dict(wh_name=wh_name, wdpaid=wdpaid, wh_geo_json=wh_geo_json)    