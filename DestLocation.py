#Author : Geraldi Dzakwan 13514065

#File yang outputnya adalah csv file berisi informasi lokasi terakhir setiap trip
#Akan ada pula visualisasi dengan chart dan map

#Cara run :
#python DestLocation.py file_input(.h5) file_output(.csv) chart_output(png) map_output(png) jumlah_sampel

#Import panda, system, csv frame, dan tiga modul lain yang sudah dibuat sebelumnya
import pandas as pd
import sys
import csv
import CoordinateToPlace as gp #Konversi koordinat ke tempat
import BasemapPortugal as bp #Gambar map
import BarChart as bc #Gambar chart

#List lokasi terakhir (destination point)
destPointList = []
#Convert ke set agar semua titik unik
#List ini nantinya akan di plot di map sehingga tidak perlu dua titik dengan koordinat sama
destPointList = set(destPointList)

#Dictionary untuk jumlah kunjungan setiap tempat dengan key adalah nama tempat
numberOfPlace2 = {}

#Inisialisasi list tempat dengan meta data
gp.initializePlaceList()

#Fungsi untuk memproses koordinat pada data frame dan kemudian 
#menambahkan kolom baru pada data frame yang berisi ID tempat bersesuaian
def processPlaceID(row):
    #Ambil x dari kolom latitude
    x = row['Latitude']
    #Ambil y dari kolom longitude
    y = row['Longitude']
    #Tentukan placeID
    placeID = gp.getPlace((x,y))[0]
    return placeID

#Fungsi untuk memproses koordinat pada data frame dan kemudian 
#menambahkan kolom baru pada data frame yang berisi nama tempat bersesuaian
def processPlaceName(row):
    #Ambil x dari kolom latitude
    x = row['Latitude']
    #Ambil y dari kolom longitude
    y = row['Longitude']
    #Tentukan placeName
    placeName = gp.getPlace((x,y))[1]
    return placeName

#Fungsi untuk inisialisasi dictionary numberOfPlace2
def initializeNumberOfPlace():
    #Buka file meta data
    with open('metaData_taxistandsID_name_GPSlocation.csv') as f:
        #Baca setiap baris
        for row in csv.reader(f):
            #Baris header tidak perlu dibaca
            if (row[0]!="ID"):
            	#Ambil koordinat x dan y dari kolom ke-2 dan 3
            	x = float(row[2])
            	y = float(row[3])
            	#Inisialisasi key dengan place ID
                #Valuenya adalah tuple jarak dari pusat kota dan frekuensi disinggahi
            	numberOfPlace2[int(row[0])] = [gp.distance_from_city_center(x,y), 0]

#Panggil fungsi inisialisasi di atas
initializeNumberOfPlace()

#Baca file h5 dan masukkan ke data frame
df = pd.read_hdf(sys.argv[1])

#Jika input jumlah sampel tidak 0 dan kurang dari total data,
#ambil sejumlah sampel tersebut dari data frame
jumlahSampel = int(sys.argv[5])
if ((jumlahSampel!=0) and (jumlahSampel<len(df))):
    df = df.sample(jumlahSampel)

#Ambil lokasi-lokasi terakhir dari data frame dan timpa isi data frame dengan 
#detail lokasi terakhir, yakni TRIP_ID, Latitude, dan Longitude
df = df.reset_index().groupby('level_0', as_index=False).last().drop('level_1', axis=1).set_index('level_0')

#Renaming kolom-kolom
df.rename(columns={'level_0': 'TRIP_ID', 'lat': 'Latitude', 'lon':'Longitude'}, inplace=True)

#Buat series yang menampung ID tempat dari masing-masing koordinat pada setiap row
series_ID = pd.Series(df.apply(processPlaceID, axis=1))
#Buat series yang menampung nama tempat dari masing-masing koordinat pada setiap row
series_Name = pd.Series(df.apply(processPlaceName, axis=1))

#Buat kolom baru PlaceID pada data frame, isi dengan series_ID
df['PlaceID'] = series_ID
#Buat kolom baru PlaceName pada data frame, isi dengan series_Name
df['PlaceName'] = series_Name

#Output data frame ke csv
df.to_csv(sys.argv[2])

#Iterasi seluruh elemen data frame
for i in range(0, len(df)):
    #Buat tuple koordinat dari setiap baris data frame
	destinationTuple = (df.iloc[i][0], df.iloc[i][1])
    #Tentukan tempat yang bersesuaian
	place = gp.getPlace(destinationTuple)
	#Update isi dictionary sesuai dengan ID tempat yang didapat
	numberOfPlace2[int(place[0])] = [numberOfPlace2[int(place[0])][0],  numberOfPlace2[int(place[0])][1]+ 1]
    #Tambahkan koordinat ke list destPoint untuk nantinya di plot ke map
	destPointList.add(destinationTuple)

#Menggambar grafik batang dan menyimpannya dalam bentuk file image
bc.destLocChart(numberOfPlace2, sys.argv[3])

#List dummy hanya untuk memenuhi argumen
labels = []

#Menggambar hasil plot pada map dan menyimpannya dalam bentuk file image
#Karena jumlah titik yang diplot sangat banyak, 
#maka setiap marker tidak diberi label nama tempat (argumen False)
bp.drawMap(destPointList, labels, False, sys.argv[4])

