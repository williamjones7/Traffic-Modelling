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
        pass
    
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
        for car in self.cars:
            pass
        #car.distance_to_next
            
