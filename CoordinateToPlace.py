#Author : Geraldi Dzakwan 13514065

#File untuk konversi koordinat ke tempat terdekat yang ada pada meta data
#Memerlukan library csv
import csv

#List kosong untuk nantinya menampung koordinat tempat
b = []

#Koordinat pusat kota porto
porto_coordinate = (41.1496100, -8.6109900)

#Fungsi untuk menghitung jarak kuadrat koordinat terhadap pusat kota
def distance_from_city_center(x, y):
	a = porto_coordinate[0] - x
	b = porto_coordinate[1] - y
	c = a*a + b*b
	return c

#Fungsi untuk membaca meta data dan mengisinya ke list
def initializePlaceList():
	#Buka file meta data
    with open('metaData_taxistandsID_name_GPSlocation.csv') as f:
    	#Baca setiap baris
        for row in csv.reader(f):
        	#Baris header tidak perlu dibaca
        	if (row[0]!="ID"):
        		#Ambil koordinat x dan y dari kolom ke-2 dan 3
        		x = float(row[2])
        		y = float(row[3])
        		#List akan berisi tuple data koordinat (x,y), placeName, placeID, dan jarak terhadap pusat kota
        		b.append((x, y, row[1], row[0], distance_from_city_center(x,y)))

#Fungsi untuk menngkonversi koordinat ke tempat terdekat
def getPlace(a):
	#Hitung Manhattan distance koordinat terhadap tempat pertama pada metadata
	selisih = abs(a[0]-b[0][0]) + abs(a[1]-b[0][1])
	#Inisialisasi return value dengan detail tempat pertama
	placeName = b[0][2]
	placeId = b[0][3]
	placeDistance = b[0][4]
	#Iterasi seluruh tempat
	for i in range(1, len(b)):
		#Hitung jaraknya terhadap koordinat
		temp = abs(a[0]-b[i][0]) + abs(a[1]-b[i][1])
		#Jika lebih kecil, maka timpa detail return value dengan detail tempat tsb
		if (temp<selisih):
			selisih = temp
			placeName = b[i][2]
			placeId = b[i][3]
			placeDistance = b[i][4]
	#Fungsi mengembalikan tuple ID, Nama, dan jarak terhadap pusat kota
	place = (int(placeId), placeName, placeDistance)
	return place