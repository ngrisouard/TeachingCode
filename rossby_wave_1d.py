# pylint: disable = invalid-name, C0111

# Solve one dimensional Rossby wave problem on a latitude circle.
import numpy as np
import matplotlib.pyplot as plt


def ddx(n, dx, f):
    """ take derivative for plotting purposes """
    fx = np.zeros(n)
    for j in range(n):
        fx[j] = (f[get_index(j+1, n)]-f[get_index(j-1, n)])/(2*dx)
    return fx


def get_index(j_in, n):
    """ get appropriate value of j in range [1,n] given j_in """
    j_out = j_in
    if j_out < 0:
        j_out = j_out + n
    elif j_out > n-1:
        j_out = j_out - n
    return j_out


def set_array(n, u, beta, tau, dx):
    """ set_array sets up finite difference array """
    # create empty n x n array
    arr = np.zeros((n, n))
    print('shape of arr = {}'.format(arr.shape))
    for j in np.arange(n):
        print('j = {}'.format(j))
        arr[j, get_index(j-1, n)] = -1./(u*tau*2*dx) + 1./dx**2
        arr[j, j] = -2./dx**2 + beta/u
        arr[j, get_index(j+1, n)] =+ 1./(u*tau*2*dx) + 1./dx**2

    return arr

a = 6.31e6  # Earth's radius
phi0 = 45.  # Reference latitude
u = 10.  # U (m/s)
g = 9.8  # g (m/s^2)
H = 10e3  # mean depth H(m)
h0 = 1e3  # mountain peak height h0(m)
dx_h = 0.2e6  # Mountain width dx_h(m), 200 km

tau = 3. * 86400  # damping time (seconds, 86400 seconds = 1 day)

A = h0 * dx_h  # A is strength of topographic forcing: h_b~A\delta(x)
x_max = 2 * np.pi * np.cos(phi0/180*np.pi)*a  # Circumference
n = 500  # Number of grid boxes
f0 = 2 * 2 * np.pi * np.sin(phi0*np.pi/180)/(86400)  # f_0
beta = 2 * 2 * np.pi * np.cos(phi0*np.pi/180)/(86400*a)  # beta

dx = x_max/n  # grid spacing
x = np.arange(-x_max/2, x_max/2, dx)  # grid from -x_max/2:x_max/2-dx

l = set_array(n, u, beta, tau, dx)
# h_b is a Gaussian mountain of height A/dx_h=h0 and width dx_h.
# In this form it approaches A\delta(x) as dx_h->0.
h_b = A * np.exp(-x**2/dx_h**2)/(np.pi**(0.5)*dx_h)
rhs = -f0 * h_b / H  # right hand side of linear equation is

# solve problem
psi = np.dot(np.linalg.inv(l), rhs.transpose())

#x in degrees for plotting purposes.
x_degrees = x * 360./x_max

plt.clf()

plt.subplot(311)
plt.plot(x_degrees, h_b)
plt.ylabel('h_b(m)')
plt.xlim([-180, 180])
plt.xticks(np.arange(-180, 210, 30))

plt.subplot(312)
plt.plot(x_degrees, psi*f0/g)
plt.xlim([-180, 180])
plt.xticks(np.arange(-180, 210, 30))
plt.ylabel('geopotential height (m)')

plt.subplot(313)
# calculate v=d(psi')/dx
v = ddx(n, dx, psi)  # ddx calculates gradient using finite difference formula
plt.plot(x_degrees, v)
plt.ylabel('meridional velocity (m/s)')
plt.xlim([-180, 180])
plt.xticks(np.arange(-180, 210, 30))
plt.ylabel('meridional velocity (m)')
plt.xlabel('longitude (degree)')

plt.show()
