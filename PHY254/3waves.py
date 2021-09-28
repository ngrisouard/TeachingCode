"""
Superposing plave waves to form wave packets
Nicolas Grisouard, University of Toronto, August 2021
"""
import numpy as np
import matplotlib.pyplot as plt


def B(A, x, dk, N):
    """x is a numpy array, dk is the inter-k separation, total number of
    modes is 2N+1"""
    numerator = np.sin((0.5+N)*x*dk)
    denominator = np.sin(0.5*x*dk)
    return A*numerator/denominator


def sum_psin(A, x, k0, dk, N):
    """dk is the separation between consecutive wavenumbers,
    2*N+1 is the number of modes"""
    psi_tot = 0*x
    for n in range(-N, N+1):
        kn = k0 + n*dk
        psi_tot += A*np.cos(kn*x)
    return psi_tot


def plot_one_figure(psi, B, k0, Dk, x, N):
    ftsz = 14  # font size

    xsc = x*k0/2/np.pi

    plt.figure(dpi=150)
    plt.plot(xsc, psi, linewidth=1., label=r'$\psi$')
    plt.plot(xsc, B, 'r--', label=r'$\pm B$')
    plt.plot(xsc, -B, 'r--')
    plt.axvline(-k0/Dk, color='k')  # vertical lines
    plt.axvline(+k0/Dk, color='k')  # vertical lines
    plt.xlim(min(xsc), max(xsc))
    plt.xlabel(r'$k_0 x/(2\pi)$', fontsize=ftsz)

    plt.legend(fontsize=ftsz)
    plt.ylabel(r'$\psi = \sum_{n=-N}^N\cos(k_n x)$', fontsize=ftsz)
    plt.title('Superposition of {} waves'.format(2*N+1), fontsize=ftsz)
    plt.grid()
    plt.tight_layout()
    plt.savefig('psi_{0}_waves.png'.format(2*N+1))

    return


# fixed parameters
A = 1.  # amplitude
k0 = 1.  # central wavenumber
Dk = k0/5  # maximum distance from k0


# Superpose 2*N+1 waves
for N in range(1, 6):
    dk = Dk/(2*N)
    x = np.linspace(-2.5*np.pi/dk, 2.5*np.pi/dk, 1024)
    psi_tot = sum_psin(A, x, k0, dk, N)
    Env = B(A, x, dk, N)  # the plus sign of the envelope
    plot_one_figure(psi_tot, Env, k0, Dk, x, N)
plt.show()
