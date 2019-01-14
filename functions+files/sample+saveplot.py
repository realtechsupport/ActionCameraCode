import os
import numpy
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

#  dl4j-examples/dl4j-examples/src/main/resources/classification/linear_data_train.csv

path = '/home/marcbohlen/try-tf-master/simdata/'
filename = 'linear_data_train.csv'
#location = path + filename
location = filename
data=numpy.genfromtxt(location,delimiter=',')
x = data[:,1]
y = data[:,2]


fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(x,y, '.')
fig.savefig('temp.png')
