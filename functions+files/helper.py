#!/usr/bin/env python
import os, sys
import numpy as np
#---------------------------------------------------------
def convert_to_fahrenheit(cvalues):
    # convert to a numpy array
    celsius = np.array(cvalues)
    #convert to Fahrenheit by scalar multiplication
    fahrenheit = (celsius * 9 / 5 + 32)
    return(fahrenheit)
#---------------------------------------------------------
def display_results(data):
    for i in range(0, len(data)):
        print data[i]
#---------------------------------------------------------
