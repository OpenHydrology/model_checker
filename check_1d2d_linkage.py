import sys
import os
'''
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.utils import *
from qgis.analysis import *
'''


from osgeo import gdal
from osgeo import osr
from osgeo import ogr



def excToStr(exc):
    import traceback
    t, n, tb = exc
    s = ''
    s += 'Type: ' + str(t) + '\n'
    s += 'Desc: ' + str(n) + '\n'
    for line in traceback.format_tb(tb):
        s += line
    return s


def genListOfIsisReaches(isisDat):
  f = open(isisDat)
  
  listOfReaches = list()
  listOfRiverNodes = list()
  
  while True:
    line = f.readline()
    #print line
    
    if line.startswith('SECTION') or line.startswith('INTERPOLATE'):
      reach = f.readline()[:12].split(' ')[0]
      length = float(f.readline()[:10])
      
      listOfRiverNodes.append(reach.strip())
      if length > 0.0:
        listOfReaches.append(reach.strip())

    
    if line.startswith('INITIAL CONDITIONS'): break
  
  listOfReaches.sort()
  listOfRiverNodes.sort()
  
  return listOfReaches,listOfRiverNodes


def loadFeatureNames(shpFile):
    items = list()
    ds = ogr.Open(shpFile)
    if ds is None:
        print 'Failed to open', shpFile
        exit(1) 
        
    tableName = os.path.basename(shpFile).split('.')[0]
    
    lyr = ds.GetLayerByName(tableName)
    
    lyr.ResetReading()
    
    geometriesList = list()
    
    for feat in lyr:
      string = feat.GetFieldAsString(0)
      #print string
      items.append(string)
      geom = feat.GetGeometryRef()
      geometriesList.append(geom.ExportToWkt())
        
    ds = None
    
    items.sort()
    
    return items

def compareLists(areTheseItems,inThisList):
  notFoundItems = list()
  for item in areTheseItems:
    if item in inThisList:
      pass
    else:
      notFoundItems.append(item)
  
  
  return    notFoundItems


def checkLinkage(tuflowNodesFile,tuflowReachesFile,isisDat):
    listOfTuflowNodes = loadFeatureNames(tuflowNodesFile)            
    #print listOfTuflowNodes
    
    listOfTulfowReaches = loadFeatureNames(tuflowReachesFile)
    #print listOfTulfowReaches
    
    listOfISISReaches,listOfISISRiverNodes = genListOfIsisReaches(isisDat)
    #print listOfISISReaches
    #print listOfISISRiverNodes
    
    notFoundReaches = compareLists(listOfTulfowReaches,listOfISISReaches)
    notFoundNodes = compareLists(listOfTuflowNodes,listOfISISRiverNodes)
    
    return notFoundReaches,notFoundNodes
    
if __name__ == '__main__':
  
  nodesFile = 'P:\\Glasgow\\WNE\\PROJECTS\\340436-Tamworth\\HydraulicModelling\\04-Initial2DBuild-July2014\\model\\SHPS\\1d_nd_RT_P.shp'
  reachesFile = 'P:\\Glasgow\\WNE\\PROJECTS\\340436-Tamworth\\HydraulicModelling\\04-Initial2DBuild-July2014\\model\\SHPS\\1d_nwk_RT_L.shp'
  isisDat = 'P:\\Glasgow\\WNE\\PROJECTS\\340436-Tamworth\\HydraulicModelling\\04-Initial2DBuild-July2014\\model\\ISIS\\Tame_at_Tamworth_v1.DAT'

  
  try:
    checkLinkage(nodesFile,reachesFile,isisDat)

  except:
    print excToStr(sys.exc_info())
