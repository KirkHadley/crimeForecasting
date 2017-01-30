import cPickle as pickle
import json
from multiprocessing import Pool
import pandas as pd
import operator
import geopandas as gpd

def dfChunker(df, chunk_size):
    splits = range(0, len(df), chunk_size)
    df_list = map(lambda x: df[x:x+chunk_size], splits)
    return df_list

def makeParallel(pdf, cores, fx, dst_path, chunk_size=None, res_fx=None, return_something=False):
    if not chunk_size:
        chunk_size = len(pdf)/cores
    df_list = dfChunker(pdf, chunk_size)
    print 'starting parallel process on %d cores' % cores
    pool = Pool(cores)
    res = pool.map(fx, df_list)
    pool.close
    pool.join()
    if res_fx:
        res = res_fx(res)
    if dst_path.endswith('pkl'):
        pickle.dump(res, open(dst_path, 'wb'))
    elif dst_path.endswith('json'):
        json.dump(res, open(dst_path, 'wb'))
    elif dst_path.endswith('shp'):
        try:
            res.to_file('dst_path')
        except:
            print "failed to save as shapefile, trying as pickle"
            pickle.dump(res, open(dstpath[:-3] + 'pkl', 'wb'))
    else:
        print 'could not infer desired file type, attempting to save as pickle'
        try:
            pickle.dump(res, open(dst_path, 'wb'))
        except:
            print 'could not save as pickle, please try again'
    if return_something:
        return res
    else:
        return 

def testfun():
    print 'hello'

