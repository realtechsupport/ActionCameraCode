#!/usr/bin/env python
import os, sys
import numpy as np
#bais numpy arrays - copy operatons
#---------------------------------------------------------
x = np.array([[42,22,12],[44,53,66]], order='F')
y = x.copy()
x[0,0] = 1001
print(x)
print(y)
