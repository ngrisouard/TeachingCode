"""
Solution to problem 10.7 of Newman
Author: Nico Grisouard, University of Toronto
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc


def f(x): return x**-0.5 / (1. + np.exp(x))


def w(x): return x**-0.5


font = {'family': 'DejaVu Sans', 'size': 14}  # adjust fonts
rc('font', **font)

N_samples = 10000  # number of samples per calculation
N_repeats = 1000  # number of times we repeat the calculation

# %% Mean Value and importance sampling Monte Carlo --------------------------|
I_MV = np.zeros(N_repeats)
I_IS = np.zeros(N_repeats)
L = 1.  # length of integration
for rr in range(N_repeats):
    for n in range(N_samples):
        z = np.random.random()
        I_MV[rr] += f(z)
        x = z**2
        I_IS[rr] += f(x)/w(x)

I_MV *= L/N_samples
I_IS *= 2./N_samples

plt.figure(dpi=150)
plt.hist(I_MV, N_repeats//10, range=[0.8, 0.88], alpha=0.5, label='Mean value')
plt.hist(I_IS, N_repeats//10, range=[0.8, 0.88],
         alpha=0.5, label='Importance sampling')
plt.xlabel('Value of integral')
plt.ylabel('Number of occurences')
plt.legend()
plt.savefig('Lab10-Q3a.pdf')
plt.show()
