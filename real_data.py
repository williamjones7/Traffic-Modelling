from lanes_basic import Road
from single_lane import Car
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import pandas as pd
import seaborn as sns

raw_data = pd.read_csv('Traffic-Modelling/Data/2014 TMU Site 11.csv')

traffic_data = raw_data

traffic_data.plot.scatter(x = ' Total Flow vehicles less than 5.2m', y = ' Speed Value', marker = '.', color = 'Navy', label = '2014 TMU Site 11 (A2) Data')

length = 4360
Nsteps = 100

def avg_speed(road):
    num_cars, sum_v, avg = 0,0,0
    for lane in road.lanes:
        for car in lane:
            if car != ' ':
                num_cars += 1
                sum_v += car.v
    if num_cars > 0:
        avg = sum_v/num_cars
    return avg * 3.6 * 4.4
    
flowrates = []
avg_speeds = []

for numsims in range(1,5):
    for flowrate in np.arange(1 + 1/numsims, 350):
        density = flowrate / length
        myroad = Road(length, density, .1, 31.2, 2)
        for t in range(Nsteps):
            myroad.timestep
        flowrates.append(flowrate)
        avg_speeds.append(avg_speed(myroad))

plt.scatter(flowrates, avg_speeds, color = 'Crimson', marker = '.', label = 'Simulated data')

plt.legend()
plt.show()
