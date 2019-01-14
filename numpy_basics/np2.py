#!/usr/bin/env python
import os, sys
import numpy as np
#bais numpy arrays - creating arrays
#---------------------------------------------------------
size = 42
x = np.array(size)
# scalars are zero dimensional arrays
print("x: ", x)
print("The type of x: ", type(x))
print("The dimension of x:", np.ndim(x))

#create one dimensional arrays
F = np.array([1, 1, 2, 3, 5, 8, 13, 21]) #integers
V = np.array([3.4, 6.9, 99.8, 12.8])     #floats
print("F: ", F)
print("V: ", V)
print("Type of F: ", F.dtype)
print("Type of V: ", V.dtype)
print("Dimension of F: ", np.ndim(F))
print("Dimension of V: ", np.ndim(V))
