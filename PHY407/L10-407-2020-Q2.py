"""
Solution to problem 10.7 of Newman
Author: Nico Grisouard, University of Toronto
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import gamma

N = int(1e6)  # make sure number of point is an integer
ND = 10  # number of dimensions (10 in 10.7)
R = 1.  # hyper-radius

# ND-D array of the coordinates of N points
points = 2.*np.random.rand(ND, N) - 1.
V = (2*R)**ND  # Volume of integration
Int = 0.  # Integral

for n in range(N):
    rad = 0.
    for i in range(ND):
        rad += points[i, n]**2
    rad = np.sqrt(rad)
    if rad <= 1:
        Int += 1.

Int *= V/N
sigma = np.sqrt(Int*(V - Int)/N)  # Note: the error would require to know the
# exact value of I. Which we do, but in reality we wouldn't.

print("  Integral =", Int)
print("     sigma =", sigma)

# Analytical formula:
IntA = (R * np.pi**0.5)**ND / gamma(0.5*ND + 1.)
sigmaA = np.sqrt(IntA*(V - IntA)/N)
print("  Analytical value: =", IntA)
print("        with sigma: =", sigmaA)
