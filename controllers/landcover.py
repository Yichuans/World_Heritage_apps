# for landcover visualisation

# ========== controller
def index():
    result = db().select(db.wh.ALL)
    return dict(result=result)


def get_landcover():
    """to be call with .csv to return csv
    see views landcover/get_landcover_csv.csv
    """
    wdpaid = request.args[0]
    landcover = db(db.landcover.wdpaid==wdpaid).select(db.landcover.lc_2000, db.landcover.lc_2010, db.landcover.areakm2)
    return dict(landcover=landcover)

def conv_matrix():
    wdpaid = request.args[0]
    wh_name = db(db.wh.wdpaid==wdpaid).select()[0].name

    return dict(wh_name=wh_name, wdpaid=wdpaid)



