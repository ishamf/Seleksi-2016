import sys
import pandas as pd
import BasemapPortugal as bp
import CoordinateToPlace as cp

destPointList = []
labels = []
cp.initializePlaceList()
#destPointList = set(destPointList)

df = pd.read_hdf(sys.argv[1])

ndf = (df * 100000).round()

cts = df.groupby(['lat', 'lon']).size()

scts = cts.sort_values()

frequent = scts.tail(5)

for i in range(0,5):
	lat = frequent.index[i][0]
	lon = frequent.index[i][1]
	coordinate = (lat,lon)
	destPointList.append(coordinate)
	labels.append(cp.getPlace(coordinate))

labels = tuple(labels)
bp.drawMap(destPointList, labels, True)
for i in range(0,5):
	print(destPointList[i])

"""
destPointList.add()

print(type(df.tail(1)['lat'][0]))

print(scts.tail(1)['lat'][0])
"""

#destPointList
#bp.drawMap(destPointList)