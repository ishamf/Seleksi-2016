import csv

b = []

porto_coordinate = (41.1496100, -8.6109900)

def distance_from_city_center(x, y):
	a = porto_coordinate[0] - x
	b = porto_coordinate[1] - y
	c = a*a + b*b
	return c

def initializePlaceList():
    with open('metaData_taxistandsID_name_GPSlocation.csv') as f:
        for row in csv.reader(f):
        	if (row[0]!="ID"):
        		x = float(row[2])
        		y = float(row[3])
        		b.append((x, y, row[1], row[0], distance_from_city_center(x,y)))

def getPlace(a):
	selisih = abs(a[0]-b[0][0]) + abs(a[1]-b[0][1])
	placeName = b[0][2]
	placeId = b[0][3]
	placeDistance = b[0][4]
	#numberOfPlace = b[0][2]
	for i in range(1, len(b)):
		temp = abs(a[0]-b[i][0]) + abs(a[1]-b[i][1])
		if (temp<selisih):
			selisih = temp
			placeName = b[i][2]
			placeId = b[i][3]
			placeDistance = b[i][4]
	place = (int(placeId), placeName, placeDistance)
	return place
	#return numberOfPlace