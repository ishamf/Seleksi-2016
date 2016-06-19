import pandas as pd
import sys
import csv
import CoordinateToPlace as gp
import BasemapPortugal as bp
import BarChart as bc

labels = []

destPointList = []
destPointList = set(destPointList)

numberOfPlace = []
numberOfPlace2 = {}
numberOfPlace3 = {}
#numberOfPlace = {}


gp.initializePlaceList()

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
            	numberOfPlace2[int(row[0])] = [gp.distance_from_city_center(x,y), 0]
        numberOfPlace.append(0)

initializeNumberOfPlace()

df = pd.read_hdf(sys.argv[1])
#df = df.iloc[df.count(level=0).lat.cumsum() - 1].reset_index().drop('level_1', axis=1).set_index('level_0')
df = df.reset_index().groupby('level_0', as_index=False).last().drop('level_1', axis=1).set_index('level_0')
df.rename(columns={'level_0': 'TRIP_ID', 'lat': 'Latitude', 'lon':'Longitude'}, inplace=True)

#df = df.sample(sys.argv[2])

for i in range(0, len(df)):
	destinationTuple = (df.iloc[i][0], df.iloc[i][1])
	place = gp.getPlace(destinationTuple)
	numberOfPlace[place[0]] = numberOfPlace[place[0]] + 1
	#Atas pake nama, bawah pake ID
	#numberOfPlace2[place[1]] = [numberOfPlace2[place[1]][0],  numberOfPlace2[place[1]][1]+ 1]
	numberOfPlace2[int(place[0])] = [numberOfPlace2[int(place[0])][0],  numberOfPlace2[int(place[0])][1]+ 1]
	destPointList.add(destinationTuple)

bc.destLocChart(numberOfPlace2, sys.argv[3])
bp.drawMap(destPointList, labels, False, sys.argv[4])

df.to_csv(sys.argv[2])
	
#print(df.iloc[0][0])