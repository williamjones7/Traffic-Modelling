class Road:
    def __init__(self, length, density, p, v_max,no_lanes,roadworks):
        self.length = length
        self.p = p
        self.density = density
        self.roadworks = roadworks
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
         
        if self.roadworks != [0,0,0]:
            self.lanes[self.roadworks[0]][self.roadworks[1]:self.roadworks[2]] = 'R'
        
            
            
    def lanechanging(self):
        
        changed_lanes = self.lanes
        gapminus = self.v_max
        
        for h in range(0,self.no_lanes):
          
            g = h+1 
            
            if g==self.no_lanes:
                g= 0
            
           
            for car in self.lanes[h]:
                if car!= ' ' and car !='R':
                    distfg=1
                    distbg=1
                    disth = 1
                    for k in range(1,self.length-car.position):
                        if self.lanes[h][car.position+k]==' ':
                            disth += 1
                        else:
                            break
                    for j in range(1,self.length-car.position):
                        if g!=9999 and self.lanes[g][car.position]==' ':
                            if self.lanes[g][car.position+j]==' ':
                                distfg+=1
                            else:
                                break
                    for o in range(1,car.position):
                        if g!=9999 and self.lanes[g][car.position]==' ':
                            if self.lanes[g][car.position-o]==' ' or self.lanes[g][car.position-0]=='R':
                                distbg+=1
                            else:
                                break
                    

                    if disth < distfg and distbg> self.v_max and car.position<self.length:
                        self.lanes[g][car.position]=car
                        car.distance_to_next = distfg
                    else:
                        car.distance_to_next=disth
            
    
    def timestep(self):
        next_lanes = np.zeros((self.no_lanes,self.length),dtype = object)
        for o in range(self.no_lanes):
            next_lanes[o]= [' '] * self.length
            
        if self.roadworks != [0,0,0]:
            next_lanes[self.roadworks[0]][self.roadworks[1]:self.roadworks[2]] = 'R'
            
        self.lanechanging()
        
        for i in range(0,self.no_lanes):
            for car in self.lanes[i]:
                if car != ' ':
                    if car != 'R':
                        car.change_speed(self.v_max,self.p)
                        car.move()
        
                        if car.position < self.length and next_lanes[i][car.position]!='R':
                            next_lanes[i][int(car.position)]=car

                        elif car.position < self.length and next_lanes[i][car.position]!='R':
                            next_lanes[i][int(car.position)] = car 
                        
                              
            if next_lanes[i][0] == ' ' and random.random() < self.density:
                next_lanes[i][0] = Car(initial_position = 0, initial_velocity = int(np.round(self.v_max*random.random())))
        
            self.lanes[i]=next_lanes[i]
                        
    def road_to_values(self):
        vals1 = []
        vals2 = []
        vals3 = []
        
        for car in self.lanes[0]:
            if car == ' ':
                vals1.append(-1)
            if car=='R':
                vals1.append(-1)
            elif car!=' ' and car!='R':
                vals1.append(car.v)
        for car in self.lanes[1]:
            if car == ' ':
                vals2.append(-1)
            if car == 'R':
                vals2.append(-1)
            if car != ' ' and car!= 'R':
                vals2.append(car.v)
        if self.no_lanes == 3:         
            for car in self.lanes[2]:
                if car == ' ':
                    vals3.append(-1)
                else:
                    vals3.append(car.v)
                
        return vals1,vals2,vals3
        
        
