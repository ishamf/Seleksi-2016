#Author : Geraldi Dzakwan 13514065

#File untuk visualisasi data dengan grafik batang
#Memerlukan library numpy dan matplotlib
import numpy as np
import matplotlib.pyplot as plt

#Buat figure dan axis dari library matplotlib
fig, ax = plt.subplots()
#List untuk menyimpan data pada sumbu x dan sumbu y
horizontalData = []
verticalData = []

#Fungsi untuk mendapatkan sebuah item tertentu pada tuple
#Digunakan nanti sebagai dasar sorting tuple
def itemgetter(*items):
    if len(items) == 1:
        item = items[0]
        def g(obj):
            return obj[item]
    else:
        def g(obj):
            return tuple(obj[item] for item in items)
    return g

#Fungsi yang menampilkan grafik batang sesuai data input
def destLocChart(numberOfPlace, output):
	#Jumlah data
	n_groups = len(numberOfPlace)

	#Ubah input dictionary menjadi list of tuple
	data = []
	for keys in numberOfPlace.keys():
		data.append((keys, numberOfPlace[keys][0], numberOfPlace[keys][1]))

	#Melakukan sorting berdasarkan jarak lokasi terhadap city center
	data = sorted(data,key=itemgetter(1))

	#Setelah di-sort, masukkan ke data untuk sumbu x dan sumbu y
	for element in data:
		horizontalData.append(element[0])
		verticalData.append(element[2])

	#Membuat tuple data sumbu y
	means = tuple(verticalData)

	#Setting tampilan/properties grafik batang, 
	#seperti ketebalan bar, warna, dan lain-lain
	index = np.arange(n_groups)
	bar_width = 0.7
	opacity = 0.4
	error_config = {'ecolor': '0.3'}

	#Membuat grafik batang berdasarkan data2 yang sudah didefinisikan sebelumnya
	rects1 = plt.bar(index, means, bar_width,
	                 alpha=opacity,
	                 color='b',
	                 error_kw=error_config,
	                 label='Place')

	#Menghilangkan tampilan skala pada sumbu x dan sumbu y
	frame1 = plt.gca()
	frame1.axes.get_xaxis().set_ticks([])
	frame1.axes.get_yaxis().set_ticks([])

	#Menampilkan judul, keterangan data sumbu x dan sumbu y beserta legenda
	plt.xlabel("Places ID")
	plt.ylabel("Trip's frequencies")
	plt.title("Trip's frequencies for each place on meta data")
	plt.legend()
	plt.tight_layout()

	#Memberi label pada setiap bar
	#Label pada sumbu x menyatakan placeID
	#Label pada sumbu x menyatakan frekuensi tempat tsb dikunjungi
	autolabel1(rects1)
	autolabel2(rects1)

	#Tampilkan dengan ukuran layar maksimum
	manager = plt.get_current_fig_manager()
	manager.resize(*manager.window.maxsize())
	#Tampilkan grafik
	plt.show()

	#Simpan grafik sesuai nama input (misalnya dalam file .png)
	fig.savefig(output, bbox_inches="tight")  

#Fungsi untuk memberi label bar pada sumbu y, yakni frekuensi dikunjungi
def autolabel1(rects):
	#Iterasi setiap bar
    for rect in rects:
    	#Ambil ketinggian
        height = rect.get_height()
        #Tampilkan nilai frekuensi pada ketinggian bar masing-masing
        ax.text(rect.get_x() + rect.get_width()/2., height,
                '%d' % int(height),
                ha='center', va='center')

#Fungsi untuk memberi label bar pada sumbu x, yakni placeID
def autolabel2(rects):
	#Iterasi setiap bar
    for rect in rects:
    	#Ambil ketinggian
        height = rect.get_height()
        #Tampilkan placeID tepat pada garis sumbu x
        ax.text(rect.get_x() + rect.get_width()/2., 0,
        		horizontalData[int(rect.get_x())],
                ha='center', va='center')

	