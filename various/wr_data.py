# write and read data from and to a file
#------------------------------
#generate phony data and save to file
#------------------------------
#import the lib
from pylab import *
from RandomArray import *
from scipy import *

# createa a data set
t = arange(0.0, 75.0, 1)
v = 0.05*t*t*t*random() - 0.3*t*t - 12*t + 700

#write it to a file
myfile = open("data.dat", "w")
for n in range(len(v)):
		myfile.write(str(v[n]))					#convert to a string
		myfile.write('\n')	
myfile.close()

#now open for reading and display
myfile = open("data.dat", "r")
mydata = myfile.read()
myfile.close()

print mydata

raw_input()
