import random
import numpy as np

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

road = Road(length=18, density=.1, p=.1, v_max=5)
print(road.cars)
road.timestep()
print(road.cars)
road.timestep()
print(road.cars)
road.timestep()
print(road.cars)
road.timestep()
print(road.cars)
road.timestep()
print(road.cars)
