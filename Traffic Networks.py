import random
import numpy as np

class Car:
    def __init__(self, initial_position, initial_velocity):
        self.position = initial_position
        self.v = initial_velocity
        self.distance_to_next = 0
    
    def __repr__(self):
        return str(self.v)
    
    def accelerate(self):
        self.v += 1
        
    def decelerate(self, new_v):
        self.v = new_v
        
    def randomise(self, p):
        if self.v > 0 and random.random() < p:
            self.v -= 1        
    
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
        for position in range(self.length):
            if random.random() < self.density:
                self.cars.append(Car(initial_position = position, initial_velocity = int(np.round(5*random.random()))))
            else:
                self.cars.append(0)
    
    def timestep(self):
        for position, car in enumerate(self.cars):
            distance_to_next = 1
            for i in range(self.length - position):
                if self.cars[i] == 0:
                    distance_to_next += 1
            car.distance_to_next = distance_to_next
            
        for position, car in enumerate(self.cars):
            
        #car.distance_to_next
