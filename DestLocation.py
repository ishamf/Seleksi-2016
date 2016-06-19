import sys
import time
import json
import csv
import numpy as np
import pandas as pd
import CoordinateToPlace as gp
import BasemapPortugal as bp
import BarChart as bc

#from utils import haversineKaggle, heading, CITY_CENTER

destPointList = []
destPointList = set(destPointList)

numberOfPlace = []
numberOfPlace2 = {}
#numberOfPlace = {}

def initializeNumberOfPlace():
    with open('metaData_taxistandsID_name_GPSlocation.csv') as f:
        for row in csv.reader(f):
            #if (row[0]!="ID"):
                #numberOfPlace[row[0]] = 0
                #numberOfPlace[row[0]] = 0
            numberOfPlace.append(0)
            numberOfPlace2[row[1]] = 0

def processRow(row):
    x = row['POLYLINE']
    if len(x)>1:
        x = np.array(x, ndmin=2)
        #data = process_trip(x[0, :], row['TIMESTAMP'])
        #data += [x[-1,1], x[-1,0], len(x)]
        destinationTuple = (x[-1,1], x[-1,0])
        place = gp.getPlace(destinationTuple)
        numberOfPlace[place[0]] = numberOfPlace[place[0]] + 1
        numberOfPlace2[place[1]] = numberOfPlace2[place[1]] + 1
        #numberOfPlace[place[1]] = numberOfPlace[place[1]] + 1
        #numberOfPlace.append(place[1])
        data = [x[-1,1], x[-1,0], place[0], place[1], len(x)]
        #data = [x[-1,1], x[-1,0], place[0], len(x)]
        destPointList.add((x[-1,1], x[-1,0]))
    else:
        data = [-1,-1,-1,-1, len(x)]
        print("len = 1 atau 0")
    return pd.Series(np.array(data))
    #return pd.Series(np.array(data, dtype=float))

t0 = time.time()
"""
FEATURES = ['wday','hour','xs','ys','d_st','heading']
"""
gp.initializePlaceList()
initializeNumberOfPlace()

print('reading training data ...')
df = pd.read_csv(sys.argv[1], converters={'POLYLINE': lambda x: json.loads(x)})#, nrows=100)

print('preparing train data ...')
ds = df.apply(processRow, axis=1)
"""
ds.columns = FEATURES + ['Destination Latitude','Destination Longitude','Number Of Points']
keep_col = ['Destination Latitude','Destination Longitude', 'Number Of Points']
ds = ds[keep_col]
"""
ds.columns = ['Destination Latitude','Destination Longitude','Place ID','Place Name', 'Number of Places Passed By']
#ds.columns = ['Destination Latitude','Destination Longitude','Place ID', 'Number of Places Passed By']
"""
df.drop(['POLYLINE','TIMESTAMP','TRIP_ID','DAY_TYPE','ORIGIN_CALL','ORIGIN_STAND'], 
        axis=1, inplace=True)
"""
df = df.join(ds)

# clean up tracks`
#df = df[(df['Destination Latitude'] != -1) & (df['MISSING_DATA']==False)]
#df.drop(['MISSING_DATA'], axis=1, inplace=True)
df.to_csv('destLocation_train.csv', index=False)

print('reading test data ...')
df = pd.read_csv('test.csv', converters={'POLYLINE': lambda x: json.loads(x)})

print('preparing test data ...')
ds = df.apply(processRow, axis=1)

ds.columns = ['Destination Latitude','Destination Longitude','Place ID','Place Name', 'Number of Places Passed By']
#ds.columns = ['Destination Latitude','Destination Longitude','Place ID', 'Number of Places Passed By']

df = df.join(ds)
df.to_csv('destLocation_test.csv', index=False)

print('Done in %.1f sec.' % (time.time()-t0))

"""
sum = 0
for keys in numberOfPlace.keys():
    sum += numberOfPlace[keys]
print("Jumlah : ")
print(sum)
"""

print(numberOfPlace2["Agra"])
print(numberOfPlace2["Alameda"])
print(numberOfPlace2["Aldoar"])

bc.destLocChart(numberOfPlace)

#bp.drawMap(destPointList)

"""

def process_row_test(row):
    x = row['POLYLINE']
    x = np.array(x, ndmin=2)
    data = process_trip(x[0, :], row['TIMESTAMP'])
    return pd.Series(np.array(data, dtype=float))

def process_trip(x, start_time):
    tt = time.localtime(start_time)
    data = [tt.tm_wday, tt.tm_hour]
    # distance from the center till cutting point
    d_st = haversineKaggle(x,  CITY_CENTER)
    head = heading(x,  CITY_CENTER[0])
    data += [x[0], x[1], d_st, head]
    return data

"""

"""
print('preparing test data ...')
ds = df.apply(process_row_test, axis=1)
ds.columns = FEATURES
df.drop(['POLYLINE','TIMESTAMP','DAY_TYPE','ORIGIN_CALL','ORIGIN_STAND',
         'MISSING_DATA'], axis=1, inplace=True)
df = df.join(ds)
df.to_csv('test_Lokasi_Terakhir_1.csv', index=False)

df['TAXI_ID'] -= np.min(df['TAXI_ID'])   # makes csv smaller -> ids in [0, 980]
"""



