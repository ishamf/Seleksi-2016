"""
Bar chart demo with pairs of bars grouped for easy comparison.
"""
import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
horizontalData = []
verticalData = []
indeksBawah = []

def itemgetter(*items):
    if len(items) == 1:
        item = items[0]
        def g(obj):
            return obj[item]
    else:
        def g(obj):
            return tuple(obj[item] for item in items)
    return g

def destLocChart(numberOfPlace, output):
	n_groups = len(numberOfPlace)

	#numberOfPlace = sorted(numberOfPlace)

	data = []
	for keys in numberOfPlace.keys():
		data.append((keys, numberOfPlace[keys][0], numberOfPlace[keys][1]))
		#horizontalData.append(keys)
		#verticalData.append(numberOfPlace[keys])

	data = sorted(data,key=itemgetter(1))

	for element in data:
		horizontalData.append(element[0])
		verticalData.append(element[2])
		print(element[1])
	
	"""
	for i in range(1,64):
		horizontalData.append(i)
		verticalData.append(numberOfPlace[i])
	"""

	means_men = tuple(verticalData)
	#std_men = tuple(verticalData)

	for i in range(1,64):
		if (i<55):
			indeksBawah.append(i)
		elif (i==55):
			indeksBawah.append(63)
		else:
			indeksBawah.append(i-1)

	index = np.arange(n_groups)
	bar_width = 0.7

	opacity = 0.4
	error_config = {'ecolor': '0.3'}

	rects1 = plt.bar(index, means_men, bar_width,
	                 alpha=opacity,
	                 color='b',
	                 #yerr=std_men,
	                 error_kw=error_config,
	                 label='Place')

	frame1 = plt.gca()
	frame1.axes.get_xaxis().set_ticks([])
	frame1.axes.get_yaxis().set_ticks([])
	plt.xlabel("Places ID")
	plt.ylabel("Trip's frequencies")
	plt.title("Trip's frequencies for each place on meta data")
	#plt.xticks(index + bar_width, int(rects1.get_x())
	#plt.xticks(index + bar_width, tuple(indeksBawah))
	plt.legend()

	plt.tight_layout()
	autolabel1(rects1)
	autolabel2(rects1)
	manager = plt.get_current_fig_manager()
	manager.resize(*manager.window.maxsize())
	plt.show()

	fig.savefig(output, bbox_inches="tight")  

def alignment(a, h):
	if (a%2==0):
		return h
	else:
		return 0

def autolabel1(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        """
        ax.text(rect.get_x() + rect.get_width()/2., height,
        		horizontalData[int(rect.get_x())],
                #'%d' % int(height),
                ha='center', va='bottom')
        """
        ax.text(rect.get_x() + rect.get_width()/2., height,# 1.05*height,#height + 3.5,
        		#indeksBawah[int(rect.get_x())],
        		#horizontalData[int(rect.get_x())],
                '%d' % int(height),
                ha='center', va='center')

def autolabel2(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        """
        ax.text(rect.get_x() + rect.get_width()/2., height,
        		horizontalData[int(rect.get_x())],
                #'%d' % int(height),
                ha='center', va='bottom')
        """
        ax.text(rect.get_x() + rect.get_width()/2., 0,#0.05*height,#2,
        		#indeksBawah[int(rect.get_x())],
        		horizontalData[int(rect.get_x())],
                #'%d' % int(height),
                ha='center', va='center')
        """
		std_men = (2, 3, 4, 1, 2)
		means_women = (25, 32, 34, 20, 25)
		std_women = (3, 5, 2, 3, 3)	
		rects2 = plt.bar(index + bar_width, means_women, bar_width,
		                 alpha=opacity,
		                 color='r',
		                 yerr=std_women,
		                 error_kw=error_config,
		                 label='Women')
		"""

	