#Solve one dimensional Rossby wave problem on a latitude circle.
from pylab import *
#Earth's radius
a=6.31e6;
#Reference latitude
phi0 = 45.
#U (m/s)
u=10.
#g (m/s^2)
g=9.81
#mean depth H(m)
H=10e3
#mountain peak height h0(m)
h0=1e3
#Mountain width dx_h(m)
dx_h=2.e5 #200 km

#damping time (seconds, 86400 seconds = 1 day)
tau=3.*86400;

#A is strength of topographic forcing: h_b~A\delta(x)
A = h0*dx_h*sqrt(pi);
#Circumference
x_max = 2.*pi*cos(phi0/180.*pi)*a;
#Number of grid boxes
n=500;
#f_0
f0=2.*2.*pi*sin(phi0*pi/180.)/(86400.);
#beta
beta=2.*2.*pi*cos(phi0*pi/180.)/(86400.*a);

#grid spacing
dx = x_max/n;
#grid from -x_max/2:x_max/2-dx
x=arange(-x_max/2,x_max/2, dx)
#take derivative for plotting purposes
def ddx(n,dx,f):
    fx = zeros(n)
    for j in range(n):
        fx[j] = (f[get_index(j+1,n)]-f[get_index(j-1,n)])/(2*dx);
    return fx

#get appropriate value of j in range [1,n] given j_in
def get_index(j_in,n):
    j_out = j_in
    if (j_out < 0):
        j_out = j_out+n
    elif (j_out > n-1):
        j_out = j_out - n
    #print j_in,j_out
    return j_out

#set_array sets up finite difference array
def set_array(n,u,beta,tau,dx):
    #create empty n x n array
    arr = zeros([n,n])
    # print 'shape arr', shape(arr)
    for j in arange(n):
        #print 'j', j
        arr[j,get_index(j-1,n)]= 1./(dx)**2 - 1./(u*tau*2*dx)
        arr[j,j] = -2./(dx)**2 + beta/u
        arr[j,get_index(j+1,n)]= 1./(dx)**2 + 1./(u*tau*2*dx)
    return arr
    
l=set_array(n,u,beta,tau,dx);
#h_b is a Gaussian mountain of height A/dx_h=h0 and width dx_h.
#In this form it approaches A\delta(x) as dx_h->0.
h_b=A*exp(-x**2/dx_h**2)/(pi**(0.5)*dx_h);
#right hand side of linear equation is 
rhs = -f0*h_b/H;

#solve problem
psi = dot(inv(l),transpose(rhs))

#x in degrees for plotting purposes.
x_degrees=x*360./x_max;

""" Plot analytical solution"""
k = sqrt(beta/u)
v_ansol = -A*f0*cos(k*x)/H
g_ansol = -A*f0**2*sin(k*x)/H/k/g #DISREPANCY IN AMPLITUDE UNEXPLAINED YET.


""" Plot """

close("all")

clf()
subplot(3,1,1)
plot(x_degrees,h_b)
ylabel('h_b(m)')
xlim([-180, 180])
xticks(arange(-180,210,30))

subplot(3,1,2)
plot(x_degrees,psi*f0/g,x_degrees,g_ansol)
xlim([-180, 180])
xticks(arange(-180,210,30))
ylabel('geopotential height (m)')


subplot(3,1,3)
#calculate v=d(psi')/dx
v=ddx(n,dx,psi);#ddx calculates gradient using finite difference formula
plot(x_degrees,v,x_degrees,v_ansol)
ylabel('meridional velocity (m/s)')
xlim([-180, 180])
xticks(arange(-180,210,30))
ylabel('meridional velocity (m)')
xlabel('longitude')

show()