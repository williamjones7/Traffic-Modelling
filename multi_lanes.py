# only works for 2 lanes at the moment but could be extended

import random
import numpy as np
import matplotlib.pyplot as plt
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
            for roadworks in self.roadworks:
                self.lanes[roadworks[0]][roadworks[1]:roadworks[2]+1] = ['R']*abs(roadworks[1] - (roadworks[2]+1))
            
      
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
            for roadworks in self.roadworks:
                next_lanes[roadworks[0]][roadworks[1]:roadworks[2]+1] = ['R']*abs(roadworks[1] - (roadworks[2]+1))
            
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


# plots

#import matplotlib.pylot as plt
# lanes = 2
# length = 500
# t_vals = np.arange(5000)
# roadworks = [0,400,401]

# my_road = Road(length = length, density = 0.1, p = 0.1 , v_max = 5, no_lanes = lanes, roadworks = roadworks)

# x_vals = np.zeros((lanes, length, len(t_vals)))

# for t in t_vals:   
#     x_vals[:,:,t] = my_road.road_to_values()
#     my_road.timestep()

# coords = []

# for l in range(lanes):
#     for t in t_vals: 
#         for p, v in enumerate(x_vals[l,:,t]):
#             if v != -1:
#                 coords.append((l, t, p, v))
            
# average_speed_by_position = np.zeros((lanes, length))
# count_by_position = np.full((lanes, length), 0.01)

# for coord in coords:
#     if coord[3] != -2:
#         average_speed_by_position[coord[0],coord[2]] += coord[3]
#         count_by_position[coord[0],coord[2]] += 1
    
# average_speed_by_position = average_speed_by_position/count_by_position
    
# fig, ax = plt.subplots()

# # for l in range(lanes):
# #     ax.plot(range(len(average_speed_by_position[l])), average_speed_by_position[l], label = "lane {}".format(l))

# ax = sns.heatmap(average_speed_by_position)

# plt.title('Heatmap of speeds for cars on a road with a roadblock at 300-301m in lane 0')
# plt.xlabel('Road Position')
# plt.ylabel('Lane')
# plt.legend()
# plt.show()



# import pandas as pd

# df = pd.DataFrame(data = coords, columns = ['l', 't', 'p', 'v'])

# df.plot.scatter(x ='p', y='t', c ='v', figsize = (16,8), colormap = 'copper', s=5)      
          
