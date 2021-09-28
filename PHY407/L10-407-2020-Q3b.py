"""
Solution to add-on to problem 10.7 of Newman
Author: Nico Grisouard, University of Toronto
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erf
from matplotlib import rc


def f(x): return np.exp(-2.*abs(x-5.))


def w(x): return np.exp(-0.5*(x-5.)**2)/np.sqrt(2*np.pi)


font = {'family': 'DejaVu Sans', 'size': 14}  # adjust fonts
rc('font', **font)

N_samples = 10000  # number of samples per calculation
N_repeats = 1000  # number of times we repeat the calculation

# %% Mean Value and importance sampling Monte Carlo --------------------------|
I_MV = np.zeros(N_repeats)
I_IS = np.zeros(N_repeats)
L = 10.  # length of integration
for rr in range(N_repeats):
    for n in range(N_samples):
        z = np.random.random()*L
        I_MV[rr] += f(z)
        x = np.random.normal(loc=5., scale=1.)
        I_IS[rr] += f(x)/w(x)


I_MV *= L/N_samples
I_IS *= erf(0.5*L/np.sqrt(2.))/N_samples

print(I_MV.mean())
print(I_IS.mean())

plt.figure(dpi=150)
plt.hist(I_MV, N_repeats//10,  range=[0.94, 1.04],
         alpha=0.5, label='Mean value')

plt.hist(I_IS, N_repeats//10,  range=[0.94, 1.04],
         alpha=0.5, label='Importance sampling')
plt.xlabel('Value of integral')
plt.ylabel('Number of occurences')
plt.legend()
plt.savefig('Lab10-Q3b.pdf')
plt.show()
