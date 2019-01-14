#!/usr/bin/env python
import os, sys
import numpy as np
#bais numpy arrays
#---------------------------------------------------------
#We have a list with values, e.g. temperatures in Celsius:
cvalues = [25.3, 24.8, 26.9, 23.9]

#Make this into a one-dimensional numpy array:
C = np.array(cvalues)
print(C)

#Turn the values into degrees Fahrenheit by scalar multiplication:
print(C * 9 / 5 + 32)
