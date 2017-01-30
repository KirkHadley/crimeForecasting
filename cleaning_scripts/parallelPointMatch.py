import cPickle as pickle
from shapely.geometry import Point, shape
import json
import operator
import geopandas as gpd
import pandas as pd
from multiprocessing import Pool

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

def parallelMatchPoints(bigDFPath, cores, chunk_size=None):
    print 'reading big df'
    pdf = pd.read_csv(bigDFPath)
    if not chunk_size:
        chunk_size = len(pdf)/cores
    splits = range(0, len(pdf), chunk_size)
    #chunks = map(lambda x: x + chunk_size, splits)
    df_list = map(lambda x: pdf[x:x+chunk_size], splits)
    'starting parallel process'
    pool = Pool(cores)
    res = pool.map(matchPoints, df_list)
    pool.close()
    pool.join()
    try:
        matched = reduce(operator.add, res)
        json.dump(matched, open('../data/cleanData/matchedPoints.json', 'wb'))
    except:
        json.dump(res, open('../data/cleanData/matchedPoints.json', 'wb'))


if __name__ == '__main__':
    #print 'reading pdf'
    #pdf = pd.read_csv('../data/cleanData/all_crim_data.csv')
    #chunk_size = 2
    #splits = range(0, len(pdf), chunk_size)
    ##chunks = map(lambda x: x + chunk_size, splits)
    #print 'splitting df'
    #df_list = map(lambda x: pdf[x:x+chunk_size], splits)
    #print 'starting matching process'
    #res = map(lambda x: matchPoints(x), df_list[:2])
    #print 'completed match'
    #matched = reduce(operator.add, res)
    #pklPath = '../data/cleanData/testmatched.pkl'
    #print 'saving %d matches in %s' % (len(matched), pklPath)
    #pickle.dump(matched, open(pklPath, 'wb'))
    #json.dump(matched, open('testmatched.json', 'wb'))
    parallelMatchPoints('../data/cleanData/all_crim_data.csv', 13) 
