import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import animation
import pandas as pd
import seaborn as sns

class Car:
    def __init__(self, initial_position, initial_velocity, number = None, initial_lane = 0):
        self.position = initial_position
        self.lane = initial_lane
        self.next_lane = self.lane
        self.location = [self.lane,self.position]
        
        self.v = initial_velocity
        self.distance_to_next = 1
        
        self.number = number
            
        # left and right
        self.forward_gap_left = [1,1]
        self.backward_gap_right = [1,1]
    
    def __repr__(self):
        return 'Car {} '.format(self.number)+'V:'+str(self.v)+' P:'+str(self.position)+' D:'+str(self.distance_to_next)
    
    def accelerate(self, v_max):
        if self.distance_to_next > self.v + 1 and v_max > self.v:
            self.v += 1
        
    def decelerate(self):
        if self.v >= self.distance_to_next:
            self.v = self.distance_to_next - 1
        
    def randomise(self, p):
        if self.v > 0 and random.random() < p:
            self.v -= 1  
            
    def change_speed(self, v_max, p):
        self.accelerate(v_max)
        self.decelerate()
        self.randomise(p)
    
    
    def move(self):
        self.position += self.v
        self.lane = self.next_lane                   
    
                        
                        
class Road:
    def __init__(self, length, density, p, v_max, no_lanes, roadworks = None):
        self.length = length
        self.p = p
        self.density = density
        self.v_max = v_max
        self.cars = []
        self.no_lanes = no_lanes
        self.lanes = [[' ' for L in range(length)] for lane in range(no_lanes)]
        self.roadworks = roadworks
        self.num = 1
        self.build_road()
        self.time = 0
        
    def __repr__(self):
            return str(self.lanes)
        
        
    def build_road(self):
        
        for i, lane in enumerate(self.lanes):
            
            distance_to_next = self.v_max+1
            position = self.length-1
            
            while 0 <= position:
                if random.random() < self.density:
                    
                    v_init = int(min(np.round(self.v_max*random.random()),distance_to_next))

                    lane[position] = Car(initial_position = position, initial_velocity = v_init, number = self.num, initial_lane = i)
                    
                    distance_to_next = 0
                
                    self.num += 1
                distance_to_next += 1
                position -= 1  
        
        if self.roadworks != None:
            for i in self.roadworks[0]:
                self.lanes[i][self.roadworks[1]:self.roadworks[2]+1] = ['R']*abs(self.roadworks[1] - (self.roadworks[2]+1))
            
      
    def distance_to_next(self, car, lane, forward = True):
        distance_to_next = 1
        if forward:
            for i in range(1, self.length - car.position):
                if self.lanes[lane][car.position + i] == ' ':
                    distance_to_next += 1
                else:
                    break
                # if at the end of the road drive off
                if car.position + i == self.length - 1:
                    distance_to_next += self.v_max
                    
            if car.position == self.length - 1:
                distance_to_next += self.v_max
        
        elif not forward:
            for i in range(1, car.position):
                if self.lanes[lane][car.position - i] == ' ' or self.lanes[lane][car.position - i] == 'R':
                    distance_to_next += 1
                else:
                    break
                # if at the start of the road 
                if car.position + i == self.length - 1:
                    # increase by one because we don't know about cars spawning in next timestep
                    distance_to_next += 1
                      
        #if car.position == self.length - 1:
            #distance_to_next += self.v_max
            
        return distance_to_next
    # lange change step before velocity change step
    # limited to only looking in one lane per timestep
    
    def new_cars(self):
        for i, lane in enumerate(self.lanes):                      
            if lane[0]==' ' and random.random() < self.density *self.v_max / 2:
                self.num += 1
                lane[0] = Car(initial_position = 0, initial_velocity = int(np.round(self.v_max*random.random())), number = self.num, initial_lane=i)

    
    def timestep(self):
        # cars look to go left on even timesteps
        left = False
        if self.time % 2 == 0:
            left = True
            
        next_lanes = [[' ' for L in range(self.length)] for lane in range(self.no_lanes)]
        
        lane_index = list(range(self.no_lanes))
            
        if self.roadworks != None:
            for i in self.roadworks[0]:
                self.lanes[i][self.roadworks[1]:self.roadworks[2]+1] = ['R']*abs(self.roadworks[1] - (self.roadworks[2]+1))
            
        # a car is in position j of lane i 
        for i, lane in enumerate(self.lanes):
            for j, car in enumerate(lane):
                if car != ' ' and car != 'R':
                    # if the neighboring lane exists
                    # left
                    if left and i+1 < self.no_lanes:
                        neighbor_lane = int(i+1)      
                    # right
                    elif not left and i-1 >= 0:
                        neighbor_lane = int(i-1)
                    
                    else:
                        neighbor_lane = i
                        
                    car.forward_gap = self.distance_to_next(car = car, lane = neighbor_lane)
                    car.backward_gap = self.distance_to_next(car = car, lane = neighbor_lane, forward = False)
                    car.distance_to_next = self.distance_to_next(car = car, lane = i)
                
                    if car.distance_to_next < car.v and car.forward_gap > car.distance_to_next:
                        weight1 = 1
                    else:
                        weight1 = 0

                    weight2 = car.v - car.forward_gap

                    weight3 = self.v_max - car.backward_gap

                    
                    car.change_speed(self.v_max, self.p)
                    
                    car.move()
                    
                    if weight1 > weight2 and weight1 > weight3 and car.position < self.length:
                        if self.lanes[neighbor_lane][car.position] == ' ':
                            car.next_lane = neighbor_lane
                    
                    
                    if car.position < self.length:
                        next_lanes[car.next_lane][car.position] = car
                        car.lane = car.next_lane
                        
        self.lanes = next_lanes
        
        self.new_cars()
                  
        self.time += 1        
            
                
    def road_to_values(self, init_lane = False):
        vals = np.full((self.no_lanes, self.length), -1)
        if init_lane:
            init_lane_ = np.full((self.no_lanes, self.length), -1)
        for i, lane in enumerate(self.lanes):
            for j, car in enumerate(lane):
                if car != ' ':
                    if car == 'R':
                        vals[i,j] = -2
                    else:
                        vals[i,j] = car.v
                        if init_lane:
                            init_lane_[i,j] = car.initial_lane
                        
        if init_lane:
            return vals, init_lane_
                
        return vals                                           
           
# checking for a few timesteps

# road = Road(length=10,density=0.2,p=0.1,v_max = 5,no_lanes=2, roadworks=[1,7,9 ])

# for i in range(5):
#     road.timestep()
#     print("Time: {}".format(road.time))
#     print(road.lanes[0])
#     print(road.lanes[1])
#     print()

# print(road.road_to_values())


#plots
lanes = 2
real_length = 1000
length = int(real_length / 7.5)
t_vals = np.arange(200)
roadworks = None

my_road = Road(length = length, density = 0.2, p = 0.3 , v_max = 5, no_lanes = lanes, roadworks=roadworks)

x_vals = np.zeros((lanes, length, len(t_vals)))

for t in t_vals:   
    x_vals[:,:,t] = my_road.road_to_values()
    my_road.timestep()

coords = []

for l in range(lanes):
    for t in t_vals: 
        for p, v in enumerate(x_vals[l,:,t]):
            if v != -1:
                coords.append((l, t, p, v))
    
# average_speed_by_position = np.zeros((lanes, length))
# count_by_position = np.full((lanes, length), 0.01)

# for coord in coords:
#     if coord[3] != -2:
#         average_speed_by_position[coord[0],coord[2]] += coord[3]
#         count_by_position[coord[0],coord[2]] += 1

# average_speed_by_position = average_speed_by_position/count_by_position
# for i in roadworks[0]:
#     average_speed_by_position[i][roadworks[1]:roadworks[2]] = -1

# fig, ax = plt.subplots(1, 1, figsize = (10, 1))


# ax = sns.heatmap(np.asarray(average_speed_by_position) * 7.5, cbar_kws={'label': 'Speed (m/s)'})
# ax = sns.heatmap(average_speed_by_position, mask= average_speed_by_position != -1, cmap='cool', cbar = False)

# ticks = list(np.linspace(0, length , 21).astype('int64'))
# tick_labels = list(np.linspace(0, real_length , 21).astype('int64'))
# ax.set_xticks([])

# plt.xlabel('Position on road')
# plt.ylabel('Lane')
# plt.legend()
# plt.show()

# fig.savefig(f'{lanes}-Heatmap', bbox_inches = 'tight')

import pandas as pd

fig, ax = plt.subplots(1, 3, figsize = (20, 5))

df = pd.DataFrame(data = coords, columns = ['l', 't', 'p', 'v'])
df['p'] = 7.5 * df['p']
df['v'] = 7.5 * df['v']

df2 = df[df['l'] == 0]
ax[1] = df2.plot.scatter(x ='p', y='t', c ='v', s=5, ax = ax[1], cmap = 'rocket', colorbar = False)      

df3 = df[df['l'] == 1]
ax[2] = df3.plot.scatter(x ='p', y='t', c ='v', s=5, ax = ax[2], cmap = 'rocket', colorbar = False)      

fig.subplots_adjust(right = 0.82)
cmap = 'rocket'
norm = mpl.colors.Normalize(vmin=0, vmax=df['v'].max())
cbar_ax = fig.add_axes([0.85, 0.1, 0.02, 0.775])
fig.colorbar(mpl.cm.ScalarMappable(norm = norm, cmap = cmap), cax = cbar_ax, label = 'Speed, m/s')

lanes = 1
real_length = 1000
length = int(real_length / 7.5)
t_vals = np.arange(200)
roadworks = None

my_road = Road(length = length, density = 0.4, p = 0.3 , v_max = 5, no_lanes = lanes, roadworks=roadworks)

x_vals = np.zeros((lanes, length, len(t_vals)))

for t in t_vals:   
    x_vals[:,:,t] = my_road.road_to_values()
    my_road.timestep()

coords = []

for l in range(lanes):
    for t in t_vals: 
        for p, v in enumerate(x_vals[l,:,t]):
            if v != -1:
                coords.append((l, t, p, v))

df = pd.DataFrame(data = coords, columns = ['l', 't', 'p', 'v'])
df['p'] = 7.5 * df['p']
df['v'] = 7.5 * df['v']

df = df[df['l'] == 0]
ax[0] = df.plot.scatter(x ='p', y='t', c ='v', s=5, ax = ax[0], cmap = 'rocket', colorbar = False)

ax[0].set_xlabel('Position, m')
ax[1].set_xlabel('Position, m')
ax[2].set_xlabel('Position, m')

ax[0].set_ylabel('Time, seconds')
ax[1].set_ylabel('Time, seconds')
ax[2].set_ylabel('Time, seconds')

ax[0].set_title('One Lane Road', fontsize = 18)
ax[1].set_title('Two Lane Road, Lane 0', fontsize = 18)
ax[2].set_title('Two Lane Road, Lane 1', fontsize = 18)

fig.savefig(f'Two-lane Diagram', bbox_inches = 'tight')


# lanes = 2
# length = 3219 
# t_vals = np.arange(100)
# roadworks = [0,500,100]
# scale = 5
# length = length * scale
# roadworks = roadworks * scale

# raw_counts = pd.read_csv('Data/dft_rawcount_local_authority_id_31.csv')

# m90data = raw_counts[raw_counts['road_name'] == 'M90']
# flows = m90data['all_motor_vehicles']
# densities = flows / length 


# fig, ax = plt.subplots(1, 1, figsize = (7,7), dpi = 200)

# Nsteps = 200

# def avg_speed(road):
#     num_cars, sum_v, avg = 0,0,0
#     for lane in road.lanes:
#         for car in lane:
#             if car != ' ' and car != 'R':
#                 num_cars += 1
#                 sum_v += car.v
#     if num_cars > 0:
#         avg = sum_v/num_cars
#     return avg * 3.6
    
# avg_speeds = []

# for density in densities:
#     myroad = Road(length, density, .1, 31.2, 2)
#     for t in range(Nsteps):
#         myroad.timestep
#     avg_speeds.append(avg_speed(myroad))

# avg_speeds_scaled = []
# for density in densities:
#     myroad = Road(length, density, .1, 31.2, 2, roadworks= roadworks)
#     for t in range(Nsteps):
#         myroad.timestep
#     avg_speeds_scaled.append(avg_speed(myroad))


# avg_speeds = np.asarray(avg_speeds) * scale
# # avg_speeds_scaled = avg_speeds + 55
# avg_speeds_scaled = np.asarray(avg_speeds_scaled) * scale

# ax.scatter(flows, avg_speeds, color = 'Green', marker = '.', label = 'No Roadworks')

# ax.scatter(flows, avg_speeds_scaled, color = 'Crimson', marker = '.', label = 'Roadworks at 500-100m')

# #find line of best fit
# a, b = np.polyfit(flows, avg_speeds, 1)

# #add line of best fit to plot
# ax.plot(flows, a*flows+b, linestyle = ':', color = 'lawngreen', label = 'Line of best fit, no roadworks')

# #find line of best fit
# a, b = np.polyfit(flows, avg_speeds_scaled, 1)

# #add line of best fit to plot
# ax.plot(flows, a*np.asarray(flows)+b, linestyle = ':', color = 'yellow', label = 'Line of best fit, roadworks')

# plt.title('A31 between the M27 J1 and the A338', fontsize = 15)
# plt.xlabel('Number of Cars on Road', fontsize = 15)
# plt.ylabel('Average Speed of Cars (km/h)', fontsize = 15)
# ax.legend()

# fig.savefig('M90 data', bbox_inches = 'tight')