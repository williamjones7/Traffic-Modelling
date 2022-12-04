from multi_lanes import Car, Road
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation, rc
import pandas as pd

# change the text format same as in the report
rc('font',**{'family':'sans-serif','sans-serif':['Computer Modern Roman'],'size':30})
rc('text', usetex=True)

raw_data = pd.read_csv('Data/2014 TMU Site 9545 (LM297).csv')

raw_data[' Total Carriageway Flow'].replace('', np.nan, inplace=True)
raw_data.dropna(subset=[' Total Carriageway Flow'], inplace=True)
traffic_data = raw_data

fig, ax = plt.subplots(1, 1, figsize = (15, 15), dpi = 200)

traffic_data.plot.scatter(x = ' Total Carriageway Flow', y = ' Speed Value', marker = '.', color = 'Navy', label = '2014 TMU Site 9545 (LM297)', ax = ax)

length = 9360
Nsteps = 200

def avg_speed(road):
    num_cars, sum_v, avg = 0,0,0
    for lane in road.lanes:
        for car in lane:
            if car != ' ' and car != 'R':
                num_cars += 1
                sum_v += car.v
    if num_cars > 0:
        avg = sum_v/num_cars
    return avg * 3.6 

# set the upper bound of the flow rate    
upper = traffic_data[' Total Carriageway Flow'].max()    
flowrates = np.arange(1, upper, 1)
avg_speeds = []
lanes = 4
for flowrate in flowrates:
    density = flowrate / (length * lanes)
    myroad = Road(length, density, .1, 31.2, 4)
    total = 0
    for t in range(Nsteps):
        myroad.timestep
    avg_speeds.append(avg_speed(myroad))

scale = 2
length = length * scale
avg_speeds_scaled = []
for flowrate in flowrates:
    density = flowrate / (length * lanes)
    myroad = Road(length, density, .1, 31.2, 4)
    total = 0
    for t in range(Nsteps):
        myroad.timestep
    avg_speeds_scaled.append(avg_speed(myroad))


avg_speeds = np.asarray(avg_speeds)
# avg_speeds_scaled = avg_speeds + 55
avg_speeds_scaled = np.asarray(avg_speeds_scaled) * scale

ax.scatter(flowrates, avg_speeds, color = 'Green', marker = '.', label = 'Simulated data, unscaled')

ax.scatter(flowrates, avg_speeds_scaled, color = 'Crimson', marker = '.', label = 'Simulated data, length and average speed scaled by 2')


#find line of best fit
a, b = np.polyfit(traffic_data[' Total Carriageway Flow'], traffic_data[' Speed Value'], 1)

#add line of best fit to plot
ax.plot(traffic_data[' Total Carriageway Flow'], a*traffic_data[' Total Carriageway Flow']+b, linestyle = ':', color = 'cyan', label = 'Line of best fit, real data')

#find line of best fit
a, b = np.polyfit(flowrates, avg_speeds, 1)

#add line of best fit to plot
ax.plot(flowrates, a*flowrates+b, linestyle = ':', color = 'lawngreen', label = 'Line of best fit, unscaled simulated data')

#find line of best fit
a, b = np.polyfit(flowrates, avg_speeds_scaled, 1)

#add line of best fit to plot
ax.plot(flowrates, a*np.asarray(flowrates)+b, linestyle = ':', color = 'yellow', label = 'Line of best fit, scaled simulated data')

#plt.title('M25 between J9 and J10')
plt.xlabel('Number of Cars on Road', fontsize=60)
plt.ylabel('Average Speed of Cars (km/h)', fontsize=60)
ax.legend(loc='upper right')

fig.savefig(f'fig/Motorway data-M25.pdf', format='pdf', bbox_inches = 'tight')

