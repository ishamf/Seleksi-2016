# Import pandas
import pandas as pd

# Import matplotlib and Basemap
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib.collections import LineCollection
from matplotlib.patches import Polygon
from matplotlib.patches import Polygon
from mpl_toolkits.basemap import Basemap

#%matplotlib inline

#import shapefile

def draw_portugal(destList, labels, islabeled):
    """
    This functions draws and returns a map of Portugal, either just of the mainland or including the Azores and Madeira islands.
    """

    latitudeList = []
    longitudeList = []
    destList = list(destList)
    print(len(destList))

    for i in range(0, len(destList)):
        latitudeList.append(destList[i][0])
        longitudeList.append(destList[i][1])

    """
    raw_data = {'latitude': [41.17714571],
            'longitude': [-8.609670271]}
    """
    raw_data = {'latitude': latitudeList, 'longitude': longitudeList}

    df = pd.DataFrame(raw_data, columns = ['latitude', 'longitude'])

    fig = plt.figure(figsize=(15.7,12.3))
    
    projection='merc'
    llcrnrlat=-80
    urcrnrlat=90
    llcrnrlon=-180
    urcrnrlon=180
    resolution='i'

    x1 = -8.8
    y1 = 41
    x2 = -8.4
    y2 = 41.3
    
    m = Basemap(projection=projection, llcrnrlat=y1, urcrnrlat=y2, llcrnrlon=x1,
                urcrnrlon=x2, resolution=resolution)
    m.drawcoastlines()
    m.drawmapboundary()
    m.drawcountries()
    m.fillcontinents(color = '#C0C0C0')

    # Define our longitude and latitude points
    # We have to use .values because of a wierd bug when passing pandas data
    # to basemap.
    x,y = m(df['longitude'].values, df['latitude'].values)

    # Plot them using round markers of size 6
    m.plot(x, y, 'ro', markersize=3)

    if (islabeled):
        labels = labels
        x_offsets = [0]*len(labels)
        y_offsets = [0]*len(labels)
 
    for label, xpt, ypt, x_offset, y_offset in zip(labels, x, y, x_offsets, y_offsets):
        plt.text(xpt+x_offset, ypt+y_offset, label)
    
    return m

def drawMap(destList, labels, islabeled):
    draw_portugal(destList, labels, islabeled)
    plt.show()