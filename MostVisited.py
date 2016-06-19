import sys
import csv
import pandas as pd
import BasemapPortugal as bp
import CoordinateToPlace as cp
import BarChart as bc

destPointList = []
labels = []
labels2 = set(labels)
numberOfPlace2 = {}
numberOfPlace = []
cp.initializePlaceList()
#destPointList = set(destPointList)

def getKeys(d, value):
	temp = []
	for key in d:
		if (d[key][1] == value):
			temp.append(key)
	return temp

def initializeNumberOfPlace():
    with open('metaData_taxistandsID_name_GPSlocation.csv') as f:
        for row in csv.reader(f):
            #if (row[0]!="ID"):
                #numberOfPlace[row[0]] = 0
                #numberOfPlace[row[0]] = 0
            if (row[0]!="ID"):
            	numberOfPlace.append(0)
            	#PlaceID, Distance, Frequencies
            	#numberOfPlace.append([row[0],gp.distance_from_city_center(x,y),0])
            	x = float(row[2])
            	y = float(row[3])
            	#Atas pake nama, bawah pake ID
            	#numberOfPlace2[row[1]] = [gp.distance_from_city_center(x,y), 0]
            	numberOfPlace2[int(row[0])] = [cp.distance_from_city_center(x,y), 0]
        numberOfPlace.append(0)

initializeNumberOfPlace()

df = pd.read_hdf(sys.argv[1])

ndf = (df * 100000).round()

cts = df.groupby(['lat', 'lon']).size()

scts = cts.sort_values()

frequent = scts.tail(sys.argv[5])

for i in range(0,sys.argv[5]):
	lat = frequent.index[i][0]
	lon = frequent.index[i][1]
	jumlah = frequent.iloc[i]
	coordinate = (lat,lon)
	place = cp.getPlace(coordinate)
	destPointList.append(coordinate)
	#numberOfPlace2[int(place[0])] = [numberOfPlace2[int(place[0])][0],  numberOfPlace2[int(place[0])][1]+ 1]
	if (numberOfPlace2[int(place[0])][1] == 0):
		labels.append(cp.getPlace(coordinate)[1])
	numberOfPlace2[int(place[0])] = [numberOfPlace2[int(place[0])][0],  numberOfPlace2[int(place[0])][1]+ jumlah]
	labels2.add(cp.getPlace(coordinate)[1])

labels = tuple(labels)
#labels2 = tuple(labels2)

keysToBeDeleted = getKeys(numberOfPlace2, int(0))

#Hapus yang jumlahnya 0
for key in keysToBeDeleted:
	del numberOfPlace2[key]

bc.destLocChart(numberOfPlace2, sys.argv[3])

bp.drawMap(destPointList, labels2, True, sys.argv[4])
#bp.drawMap(destPointList, labels2, False, sys.argv[4])
for i in range(0,10):
	print(destPointList[i])

frequent.to_csv(sys.argv[2])

"""
destPointList.add()

print(type(df.tail(1)['lat'][0]))

print(scts.tail(1)['lat'][0])
"""

#destPointList
#bp.drawMap(destPointList)