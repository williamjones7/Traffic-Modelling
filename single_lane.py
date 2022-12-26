import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import pandas as pd

class Car:
    def __init__(self, initial_position, initial_velocity):
        self.position = initial_position
        self.v = initial_velocity
        self.distance_to_next = 1
    
    def __repr__(self):
        return 'V:'+str(self.v)+' P:'+str(self.position)
    
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
        
        
class Road:
    def __init__(self, length, density, p, v_max):
        self.length = length
        self.p = p
        self.density = density
        self.v_max = v_max
        self.cars = []
        self.build_road()
        
    def __repr__(self):
        return str(self.cars)
        
    def build_road(self):
        distance_to_next = self.v_max + 1
        position = self.length-1

        self.cars = [' ' for L in range(self.length)]
        
        while 0 <= position:
            if random.random() < self.density:
                v_init = int(min(np.round(self.v_max*random.random()), distance_to_next))
                self.cars[position] = Car(initial_position = position, initial_velocity = v_init)
                distance_to_next = 0
            distance_to_next += 1
            position -= 1
            
    def distance_to_next(self, car):
        distance_to_next = 1
        for i in range(1, self.length - car.position):
            
            if self.cars[car.position + i] == ' ':
                distance_to_next += 1
            else:
                break
            
            if car.position + i == self.length - 1:
                distance_to_next += self.v_max
        
        if car.position == self.length - 1:
            distance_to_next += self.v_max
            
        car.distance_to_next = distance_to_next

    def timestep(self):
        # assigning car distances
        for car in self.cars:
            if car != ' ':
                self.distance_to_next(car)
        
        # making copy for new road
        next_road = [' '] * self.length
        
        # move cars
        for car in self.cars:
            # if not an empty slot
            if car != ' ':
                car.change_speed(self.v_max, self.p)
                car.move()
                # think I need to add 1 here
                if car.position < self.length:
                    next_road[car.position] = car
           
        # new car entering
        if next_road[0] == ' ' and random.random() < self.density:
            next_road[0] = Car(initial_position = 0, initial_velocity = int(np.round(self.v_max*random.random())))
        
        self.cars = next_road
        
    def road_to_values(self):
        vals = []
        for car in self.cars:
            if car == ' ':
                vals.append(-1)
            else:
                vals.append(car.v)
        return vals

#Plotting

t_vals = np.arange(101)

my_road = Road(length = 1000, density = .2, p = .1, v_max = 10)

x_vals = []

for t in t_vals:   
    x_vals.append(my_road.road_to_values())
    my_road.timestep()

#generating coordinates
coords = []

for t in t_vals:
    for p, x in enumerate(x_vals[t]):
        if x != -1:
            coords.append((t, p, x))

df = pd.DataFrame(data = coords, columns = ['t', 'p', 'v'])
df.head()

# def animation_function(t):
#     plt.clf()
#     data = df.loc[df['t'] == t]
#     positions = data['p']
#     speeds = data['v']
#     plt.scatter(positions, np.zeros(len(speeds)), c = speeds, s = 30)
#     plt.xlim([0,500])

fig = plt.figure(figsize=(5,5))
# anim = animation.FuncAnimation(fig, animation_function, frames = 100, interval = 1)

df.plot.scatter(x ='p', y = 't', c ='v', figsize = (5,5), colormap = 'inferno', s=30, marker = '.')

plt.show()