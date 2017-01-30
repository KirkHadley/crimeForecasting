from shapely.geometry import Point, shape
import operator
from utils import makeParallel

GEO_DF_PATH = "../data/shapefiles/intersections.shp"

def matchPoints(bigDF):
    geoDF =  gpd.GeoDataFrame.from_file(GEO_DF_PATH) 
    squares = []
    for i in range(len(bigDF)):
        if i % 10000 == 0:
            print 'on row %d, %f percent complete' % (i, float(i)/float(len(bigDF)))
        coord = bigDF.iloc[i][['x_coordinate', 'y_coordinate']]
        pt = Point(coord['x_coordinate'], coord['y_coordinate'])
        g = geoDF[geoDF.geometry.contains(pt) == True]['geometry']
        if len(g) > 0:
            squares.append({'df_index':i, 'square_index': g.index.values[0]})
        else:
            squares.append({'df_index':i, 'square_index': None})
        print 'COMPLETED %d rows, %f percent complete' % (i+1, float(i+1)/float(len(bigDF)))
    return squares

def reduceDFList(df_list):
    return reduce(operator.add, df_list)

def nestedListToGeoDF(df_list):
    flattened = reduceDFList(df_list)
    cols = flattened[0].keys()
    geoDF = gpd.GeoDataFrame(flattened, columns=cols)
    return geoDF

def findIntersections(districtsDF):
    data = []
    bigGeoDF = gpd.GeoDataFrame.from_file("../data/shapefiles/polyGrid.shp")
    for i in range(len(districtsDF)):
        print 'on row %d, %f percent complete' % (i, float(i)/float(len(bigDF)))
        for y in range(len(g3)):
            if districtsDF.iloc[i]['geometry'].intersects(bigGeoDF.iloc[y]['geometry']):
                data.append({'geometry': districtsDF.iloc[i]['geometry'].intersection(bigGeoDF.iloc[y]['geometry']), 
                    'district':districtsDF.iloc[i]['DISTRICT'], 
                    'precinct': districtsDF.iloc[i]['PRECINCT']})
    return data


