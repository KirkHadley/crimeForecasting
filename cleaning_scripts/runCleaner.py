"""Run a specified step of the cleaner, or choose all

Usage:
  runCleaner.py intersections [--input=<shapefilePath>] [--dest=<outputShapefile>]
  runCleaner.py match [--input=<csvPath>] [--dest=<outputShapefile>]
  runCleaner.py (-h | --help)

Examples:
  runCleaner.py intersections # will run parallelIntersections
  runCleaner.py match # will run parallelPointsToSquares

Options:
  -h, --help
  --input=<path>  Path to input data 
  --dest=<path>  Path to output file 
"""
from cleaningFuncs import *
from utils import *
import geopandas as gpd
import pandas as pd
from docopt import docopt

def parallelIntersections(districtDFPath=None, dst_path=None):
    if not bigDFPath:
        districtDFPath='../data/shapefiles/Portland_Police_Districts.shp'
    if not dst_path:
        dst_path='../data/shapefiles/intersections.shp'
    gdf = gpd.GeoDataFrame.from_file(districtsDFPath)
    res = makeParallel(gdf, cores, findIntersections, dst_path=dst_path, res_fx=nestedListToGeoDF, )

def parallelPointsToSquares(bigDFPath=None, dst_path=None):
    if not bigDFPath:
        bigDFPath='../data/cleanData/all_crim_data.csv'
    if not dst_path:
        dst_path='../data/cleanData/matchedPoints.json'
    pdf = pd.read_csv(bigDFPath)
    res = makeParallel(gdf, cores, matchPoints, dst_path, res_fx=reduceDFList)


if __name__=='__main__':
    arguments = docopt(__doc__, version='0.1.1rc')
    if arguments['match']:
        parallelPointsToSquares(arguments['--input'], arguments['--dest'])
    elif arguments['intersections']:
        parallelIntersections(arguments['--input'], arguments['--dest'])
    else:
        print "Please choose a cleaning step to run. See -h for more"
