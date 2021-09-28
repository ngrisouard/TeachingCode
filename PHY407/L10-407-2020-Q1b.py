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


font = {'family': 'DejaVu Sans', 'size': 16}  # adjust fonts
rc('font', **font)
dpi = 150  # dots per inch


# %% main program starts here ------------------------------------------------|


plt.ion()

Lp = 101  # size of domain
N = 1000  # number of particles
# array to represent whether each gridpoint has an anchored particle
anchored = np.zeros((Lp, Lp), dtype=int)
# list to represent x and y positions of anchored points
anchored_points = [[], []]
centre_point = (Lp-1)//2  # middle point of domain

# set up animation of anchored points
animation_interval = 1  # how many moves to make before updating plot of
# DLA. Increase to only show anchoring events.
plt.figure(1, dpi=dpi)
plt.title('DLA run for 100 particles')
moving_plot = plt.plot(centre_point, centre_point, '.r', markersize=10)
anchored_plot = plt.plot(anchored_points[0],
                         anchored_points[1], '.k', markersize=10)

plt.xlim([-1, Lp])
plt.ylim([-1, Lp])
plt.xlabel('$x$')
plt.ylabel('$y$')

for j in range(N):
    xp = centre_point
    yp = centre_point
    i = 0  # counter to keep track of animation of moving particle

    still_moving = True
    while still_moving:
        if xp == 0 or xp == Lp-1 or yp == 0 or yp == Lp-1:
            # Check if the particle has reached a wall
            anchored[xp, yp] = 1
            anchored_points[0].append(xp)
            anchored_points[1].append(yp)
            anchored_plot[0].set_xdata(anchored_points[0])
            anchored_plot[0].set_ydata(anchored_points[1])
            plt.draw()
            plt.pause(0.001)
            still_moving = False
        # Check if particle is adjacent to an anchored particle
        elif anchored[xp-1:xp+2, yp-1:yp+2].any():
            # array above has shape (3, 3). The .any() method will return 1 if
            # an anchored particle is present in that tile.
            anchored[xp, yp] = 1
            anchored_points[0].append(xp)
            anchored_points[1].append(yp)
            anchored_plot[0].set_xdata(anchored_points[0])
            anchored_plot[0].set_ydata(anchored_points[1])
            plt.draw()
            plt.pause(0.001)
            still_moving = False
        else:  # If neither of the above, move particle and continue while loop
            i += 1
            xp, yp = nextmove(xp, yp)
            if i % animation_interval == 0:
                moving_plot[0].set_xdata(xp)
                moving_plot[0].set_ydata(yp)
                plt.draw()
                # plt.pause(0.001)
