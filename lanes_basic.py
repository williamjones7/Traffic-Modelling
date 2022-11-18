class Road:
    def __init__(self, length, density, p, v_max,no_lanes):
        self.length = length
        self.p = p
        self.density = density
        self.v_max = v_max
        self.lanes = []
        self.cars = []
        self.no_lanes = no_lanes
        self.build_road()
        
    def __repr__(self):
            return str(self.lanes)

        
        
    def build_road(self):
        distance_to_next = self.v_max+1
        position = self.length-1 
            
        self.lanes = np.zeros((self.no_lanes,self.length),dtype = object)
        lane= [' ' for L in range(self.length)]
            
        for i in range(0,self.no_lanes):
            self.lanes[i]=lane
            
                
            
        while 0<=position:
            if random.random()<self.density:
                for i in range(0,self.no_lanes):
                    v_init = int(min(np.round(self.v_max*random.random()),distance_to_next))
                        
                    self.lanes[i][position] = Car(initial_position = position, initial_velocity = v_init)
                    distance_to_next = 0
            distance_to_next += 1
            position -= 1
            
    
    
    def distance_to_next(self, car, lane):
        distance_to_next =1 
        
        for k in range(1,self.length-car.position):
            if self.lanes[lane, car.position + k] == ' ':
                distance_to_next +=1
            else:
                break
            
            if car.position + k == self.length -1:
                distance_to_next += self.v_max
            
        if car.position == self.length-1:
            distance_to_next += self.v_max
                
        car.distance_to_next = distance_to_next
    
    
    
    
    
    def timestep(self):
        #assign car distances
        for i in range(0,self.no_lanes):
            for k in range(0,self.length-1):
                if self.lanes[i][k] != ' ':
                    #self.lanes[i][k].distance_to_next = 1
                    self.distance_to_next(car = self.lanes[i][k],lane = i)
            
        next_lanes = np.zeros((self.no_lanes,self.length),dtype = object)
        for o in range(self.no_lanes):
            next_lanes[o]= [' '] * self.length
                
                
            ### MOVEMENT
            
        for g in range(self.no_lanes):
            for car in self.lanes[g]:
                if car != ' ':
                    car.change_speed(self.v_max,self.p)
                    car.move()
                    
                    if car.position < self.length:
                        next_lanes[g][car.position]= car
                        
                              
            if next_lanes[g][0] == ' ' and random.random() < self.density:
                next_lanes[g][0] = Car(initial_position = 0, initial_velocity = int(np.round(self.v_max*random.random())))
        
            self.lanes[g]=next_lanes[g]

    def road_to_values(self):
        vals1 = []
        vals2 = []
        vals3 = []
        
        for car in self.lanes[0]:
            if car == ' ':
                vals1.append(-1)
            else:
                vals1.append(car.v)
        for car in self.lanes[1]:
            if car == ' ':
                vals2.append(-1)
            else:
                vals2.append(car.v)
                
        for car in self.lanes[2]:
            if car == ' ':
                vals3.append(-1)
            else:
                vals3.append(car.v)
                
        return vals1,vals2,vals3
        
