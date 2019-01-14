#!/usr/bin/env python
import os, sys
import numpy as np
#bais numpy arrays - multidimensional arrays (matrices)
#---------------------------------------------------------
F = np.array([1, 1, 2, 3, 5, 8, 13, 21, 34, 55])
A = np.array([ [3.4, 8.7, 9.9, 11.1],
               [1.1, -7.8, -0.7, -0.5],
               [4.1, 12.3, 4.8, 5.6]])
print(A)
print(A.ndim)
#find the shape of the matrix
print(np.shape(A))

# print the first element of F, i.e. the element with the index 0
print(F[0])
# print the last element of F
print(F[-1])

#similarly for the 2d matrix
print(A[0][0])
# print the last element of F
print(A[-1][-1])

#select certain parts of the array or matrix
print(F[2:5])
print(F[:4])
print(F[6:])
print(F[:])
print(A[:2,2:])
print(A[::2, ::3])
