import csv

b = []

def initializePlaceList():
    with open('metaData_taxistandsID_name_GPSlocation.csv') as f:
        for row in csv.reader(f):
        	if (row[0]!="ID"):
        		x = float(row[2])
        		y = float(row[3])
        		b.append((x, y, row[1], row[0]))

def getPlace(a):
	selisih = abs(a[0]-b[0][0]) + abs(a[1]-b[0][1])
	placeName = b[0][2]
	placeId = b[0][3]
	#numberOfPlace = b[0][2]
	for i in range(1, len(b)):
		temp = abs(a[0]-b[i][0]) + abs(a[1]-b[i][1])
		if (temp<selisih):
			selisih = temp
			placeName = b[i][2]
			placeId = b[i][3]
	place = (int(placeId), placeName)
	return place
	#return numberOfPlace