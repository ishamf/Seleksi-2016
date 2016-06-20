#Author : Geraldi Dzakwan 13514065

#File untuk menggambarkan/plotting koordinat pada map kota Porto

# Import library pandas
import pandas as pd

# Import library numpy, matplotlib, dan basemap
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib.collections import LineCollection
from matplotlib.patches import Polygon
from matplotlib.patches import Polygon
from mpl_toolkits.basemap import Basemap

#Fungsi yang mengembalikan map kota Porto
def draw_portugal(destList, labels, islabeled, output):
    #List latitude koordinat
    latitudeList = []
    #List langitude koordinat
    longitudeList = []
    #Convert destList dari tipe set ke list
    destList = list(destList)

    #Pecah tuple destList menjadi dua list latitude dan longitude
    #Iterasi destList
    for i in range(0, len(destList)):
        #Masukkan data ke latitudeList dan longitudeList
        latitudeList.append(destList[i][0])
        longitudeList.append(destList[i][1])

    #Buat dictionary berisi list dengan key masing2 untuk list latitude dan longitude
    raw_data = {'latitude': latitudeList, 'longitude': longitudeList}  

    #Buat DataFrame yang akan di-plot sesuai dengan dictionary
    df = pd.DataFrame(raw_data, columns = ['latitude', 'longitude'])

    #Buat figure map yang akan ditampilkan berikut sizenya
    fig = plt.figure(figsize=(15.7,12.3))
    #Detail map 
    #Resolution dan projection
    projection='merc'
    resolution='i'

    #Area map yang ditampilkan
    #Mengambil area di sekitar Porto, Portugal
    x1 = -8.8 #minimum longitude 
    y1 = 41 #minimum latitude
    x2 = -8.4 #maksimum longitude
    y2 = 41.3 #maksimum latitude
    
    #Buat map dengan lower left corner dan upper right corner dari latitude dan longitude,
    #, projection, dan resolution yang sudah didefinisikan sebelumnya
    m = Basemap(projection=projection, llcrnrlat=y1, urcrnrlat=y2, llcrnrlon=x1,
                urcrnrlon=x2, resolution=resolution)
    #Detail lain seperti garis pantai, batas negara, warna, dll
    m.drawcoastlines()
    m.drawmapboundary()
    m.drawcountries()
    m.fillcontinents(color = '#C0C0C0')

    #Buat koordinat x,y dari dataframe untuk nantinya di-plot
    x,y = m(df['longitude'].values, df['latitude'].values)

    #Plotting dengan koordinat x,y
    #Gunakan market bulat(round) dengan ukuran 3
    m.plot(x, y, 'ro', markersize=3)

    #Labeling marker dengan nama tempat untuk MostVisited saja, DestLoc tidak
    if (islabeled):
        labels = labels
        #Setting offset (jarak label dengan marker)
        x_offsets = [0]*len(labels)
        y_offsets = [0]*len(labels)
 
        #Plotting label ke marker yang sesuai
        for label, xpt, ypt, x_offset, y_offset in zip(labels, x, y, x_offsets, y_offsets):
            plt.text(xpt+x_offset, ypt+y_offset, label)
    
    #Tampilkan dengan ukuran layar maksimum
    manager = plt.get_current_fig_manager()
    manager.resize(*manager.window.maxsize())

    #Simpan grafik sesuai nama input (misalnya dalam file .png)
    fig.savefig(output, bbox_inches="tight")

    #return BaseMap
    return m

#Fungsi yang dipanggil pada modul lain untuk menggambar map
def drawMap(destList, labels, islabeled, output):
    #Panggil fungsi yang mereturn basemap
    draw_portugal(destList, labels, islabeled, output)
    #Tampilkan map dengan library basemap matplotlib
    plt.show()