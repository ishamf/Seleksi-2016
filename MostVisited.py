#Author : Geraldi Dzakwan 13514065

#File yang outputnya adalah csv file berisi informasi beberapa lokasi yang paling
#sering disinggahi saat perjalanan (sesuai dengan konfirmasi dari asisten bahwa seluruh
#titik lokasi harus diperhitungkan)
#Akan ada pula visualisasi dengan chart dan map

#Cara run :
#python MostVisited.py file_input(.h5) file_output(.csv) chart_output(png) map_output(png) jumlah_sampel jumlah_koordinat_paling_sering_yang_diambil

#Import panda, system, csv frame, dan tiga modul lain yang sudah dibuat sebelumnya
import pandas as pd
import sys
import csv
import CoordinateToPlace as cp #Konversi koordinat ke tempat
import BasemapPortugal as bp #Gambar map
import BarChart as bc #Gambar chart

#List lokasi terakhir (destination point)
destPointList = []
#Tidak perlu di-convert ke set karena program pasti akan melakukan append koordinat unik

#Dictionary untuk jumlah kunjungan setiap tempat dengan key adalah nama tempat
numberOfPlace2 = {}

#Inisialisasi list tempat dengan meta data
cp.initializePlaceList()

#List untuk menampung label tempat yang nantinya menjadi keterangan marker di map
labels = []

#Fungsi untuk mendapatkan list of key dari value tertentu pada suatu dictionary
def getKeys(d, value):
    #Buat list kosong
	temp = []
    #Iterasi list input dengan keynya
	for key in d:
        #Jika isi elemen kedua dari tuple sama dengan value
		if (d[key][1] == value):
            #Masukkan key ke return value
			temp.append(key)
	return temp

#Fungsi untuk memproses koordinat pada data frame dan kemudian 
#menambahkan kolom baru pada data frame yang berisi ID tempat bersesuaian
def processPlaceName(row):
    #Ambil x dari isi tuple pertama (latitude)
    x = row.name[0]
    #Ambil x dari isi tuple pertama (longitude)
    y = row.name[1]
    #Tentukan placeName
    placeName = cp.getPlace((x,y))[1]
    return placeName

#Fungsi untuk memproses koordinat pada data frame dan kemudian 
#menambahkan kolom baru pada data frame yang berisi nama tempat bersesuaian
def processPlaceID(row):
    #Ambil x dari isi tuple pertama (latitude)
    x = row.name[0]
    #Ambil x dari isi tuple pertama (longitude)
    y = row.name[1]
    #Tentukan placeID
    placeID = cp.getPlace((x,y))[0]
    return placeID

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
            	numberOfPlace2[int(row[0])] = [cp.distance_from_city_center(x,y), 0]

#Panggil fungsi inisialisasi di atas
initializeNumberOfPlace()

#Baca file h5 dan masukkan ke data frame
df = pd.read_hdf(sys.argv[1])

#Jika input jumlah sampel tidak 0 dan kurang dari total data,
#ambil sejumlah sampel tersebut dari data frame
jumlahSampel = int(sys.argv[5])
if ((jumlahSampel!=0) and (jumlahSampel<len(df))):
    df = df.sample(jumlahSampel)

#Lakukan grouping data frame berdasarkan koordinat (latitude, longitude)
#Kemudian, untuk setiap grup koordinat hitung jumlah baris datanya
cts = df.groupby(['lat', 'lon']).size()

#Sort koordinat berdasarkan jumlah kemunculannya
#Sort secara menurun, koordinat dengan jumlah kemunculan terbanyak berada di atas series
scts = cts.sort_values(ascending=False)

#Buat series baru frequent
#Isi series frequent dengan sejumlah koordinat teratas (sejumlah koordinat yang paling banyak disinggahi)
#Jumlah koordinat yang diambil bergantung pada input
frequent = scts.head(int(sys.argv[6]))

#Iterasi koordinat2 pada frequent
for i in range(0,int(sys.argv[6])):
    #Ambil latitude
	lat = frequent.index[i][0]
    #Ambil longitude
	lon = frequent.index[i][1]
    #Ambil jumlah kemunculan
	jumlah = frequent.iloc[i]
    #Buat koordinat
	coordinate = (lat,lon)
    #Tentukan tempat yang bersesuaian
	place = cp.getPlace(coordinate)
    #Tambahkan koordinat ke list untuk nantinya di-plot ke map
	destPointList.append(coordinate)
    #Tambahkan label untuk setiap tempat hanya apabila belum pernah ditambahkan sebelumnya
    #(jumlah kemunculannya masih nol dan baru mau ditambahkan)
	if (numberOfPlace2[int(place[0])][1] == 0):
		labels.append(cp.getPlace(coordinate)[1])
    #Update isi dictionary sesuai dengan ID tempat yang didapat
	numberOfPlace2[int(place[0])] = [numberOfPlace2[int(place[0])][0],  numberOfPlace2[int(place[0])][1]+ jumlah]

#Ubah series ke frame
frequent = frequent.to_frame()

#Buat series yang menampung ID tempat dari masing-masing koordinat pada setiap row
series_ID = pd.Series(frequent.apply(processPlaceID, axis=1))
#Buat series yang menampung nama tempat dari masing-masing koordinat pada setiap row
series_Name = pd.Series(frequent.apply(processPlaceName, axis=1))

#Gabungkan frequent dengan kedua series baru tsb
frequent = pd.concat([frequent, series_ID, series_Name], axis=1)
#Rename kolom-kolom
frequent.columns = ['Frequency', 'PlaceID', 'PlaceName']

#Output data frame ke csv
frequent.to_csv(sys.argv[2])

#Buat list keysToBeDeleted
#List ini menampung semua key yang valuenya pada dictionary numberOfPlace2 adalah 0
#Artinya placeID ini tidak muncul sebagai koordinat paling sering dikunjungi
#(frekuensi kemunculannya nol)
keysToBeDeleted = getKeys(numberOfPlace2, int(0))

#Iterasi key pada list deleted
for key in keysToBeDeleted:
    #Hapus elemen dictionary dengan key tsb
	del numberOfPlace2[key]

#Menggambar grafik batang dan menyimpannya dalam bentuk file image
bc.destLocChart(numberOfPlace2, sys.argv[3])

#Cast label menjadi tuple sebagai argumen untuk plotting Map
labels = tuple(labels)

#Menggambar hasil plot pada map dan menyimpannya dalam bentuk file image
#Karena jumlah titik yang diplot sedikit, 
#maka setiap marker diberi label nama tempat (argumen True)
bp.drawMap(destPointList, labels, True, sys.argv[4])