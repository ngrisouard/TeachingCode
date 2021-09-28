# Solution to problem 10.3 of Newman
# Author: Nico Grisouard, University of Toronto
# Date: 14 November 2018

from random import randrange
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc


def nextmove(x, y):
    """ randomly choose a direction
    0 = up, 1 = down, 2 = left, 3 = right"""
    direction = randrange(4)

    if direction == 0:  # move up
        y += 1
    elif direction == 1:  # move down
        y -= 1
    elif direction == 2:  # move right
        x += 1
    elif direction == 3:  # move left
        x -= 1
    else:
        print("error: direction isn't 0-3")

    return x, y


font = {'family': 'DejaVu Sans', 'size': 14}  # adjust fonts
rc('font', **font)
dpi = 150  # dots per inch

# %% main program starts here ------------------------------------------------|
plt.ion()

Lp = 101  # size of domain
N = 1  # number of particles
Nt = 5000  # max number of steps
# list to represent x and y positions of anchored points
centre_point = (Lp-1)//2  # middle point of domain

# set up animation
animation_interval = 500  # how many moves to make before updating plot of
# Brownian motion
plt.figure(1, dpi=dpi)  # if animated
plt.title('Brownian motion for 1 particle')
moving_plot = plt.plot(centre_point, centre_point, '.r', markersize=10)
plt.xlim([-1, Lp])
plt.ylim([-1, Lp])
plt.xlabel('$x$')
plt.ylabel('$y$')

xpos = np.empty(Nt)
ypos = np.empty(Nt)

xp = centre_point
yp = centre_point

for i in range(Nt):
    xpp, ypp = nextmove(xp, yp)  # make a move
    if xp == 0:  # Check if the particle had reached left wall
        if yp == 0:  # it had also reached bottom left corner
            print("  bottom left corner hit")  # to check it works
            while xpp < 0 or ypp < 0:  # that's if it ran into wall
                xpp, ypp = nextmove(xp, yp)
        elif yp == Lp-1:  # top left corner
            print("  top left corner hit")  # to check it works
            while xpp < 0 or ypp > Lp-1:  # that's if it ran into wall
                xpp, ypp = nextmove(xp, yp)
        else:  # It had just reached the wall
            while xpp < 0:
                xpp, ypp = nextmove(xp, yp)
        xp, yp = xpp, ypp
    elif xp == Lp-1:  # Check if the particle has reached right wall
        if yp == 0:  # it had also reached bottom right corner
            print("  bottom right corner hit")  # to check it works
            while xpp > Lp-1 or ypp < 0:  # that's if it ran into wall
                xpp, ypp = nextmove(xp, yp)
        elif yp == Lp-1:  # top right corner
            print("  top right corner hit")  # to check it works
            while xpp > Lp-1 or ypp > Lp-1:  # that's if it ran into wall
                xpp, ypp = nextmove(xp, yp)
        else:  # It had just reached the wall
            while xpp > Lp-1:
                xpp, ypp = nextmove(xp, yp)
        xp, yp = xpp, ypp
    elif yp == 0:  # Check if the particle has reached bottom wall
        # Note: we have treated the corners already
        while ypp < 0:  # that's if it ran into wall
            xpp, ypp = nextmove(xp, yp)
        xp, yp = xpp, ypp
    elif yp == Lp-1:  # Check if the particle has reached top wall
        # Note: we have treated the corners already
        while ypp > Lp-1:  # that's if it ran into wall
            xpp, ypp = nextmove(xp, yp)
        xp, yp = xpp, ypp
    else:  # If neither of the above, move particle and continue for loop
        xp, yp = xpp, ypp

    xpos[i], ypos[i] = xp, yp

    if i % animation_interval == 0:
        moving_plot[0].set_xdata(xp)
        moving_plot[0].set_ydata(yp)
        plt.draw()
        plt.pause(0.001)

plt.figure(2, dpi=dpi)
plt.plot(xpos, ypos)
plt.title('Brownian motion for 1 particle')
plt.axis('scaled')
plt.xlim([-1, Lp])
plt.ylim([-1, Lp])
plt.xlabel('$x$')
plt.ylabel('$y$')
plt.savefig('Lab10-Q1a.pdf')
