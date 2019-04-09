#------------------------------------------------------------------------------+
#
#   Nathan A. Rooy
#   Simple Particle Swarm Optimization (PSO) with Python
#   July, 2016
#
#------------------------------------------------------------------------------+

#--- IMPORT DEPENDENCIES ------------------------------------------------------+

from __future__ import division
import random
import numpy
import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#--- COST FUNCTION ------------------------------------------------------------+

# function we are attempting to optimize (minimize)
def func1(x):
    total=0
    for i in range(len(x)):
        total+=x[i]**2
    return total

def function1(x): #f(0,0,...0) = 0
    total=0
    for i in range(len(x)):
        total+= (x[i])**2
    return total

def function2(coord): #Beale Function: f(3,0.5) = 0
    x = coord[0]
    y = coord[1]

    f = (1.5-x+(x*y))**2+(2.25-x+(x*(y**2)))**2+(2.625-x+(x*(y**3)))**2
    return f

def function3(coord): #Levi Function: f(1,1) = 0
    x = coord[0]
    y = coord[1]
    pi = math.pi
    f = ((math.sin(3*pi*x))**2)+((x-1)**2)*(1+(math.sin(3*pi*y))**2)+((y-1)**2)*(1+(math.sin(2*pi*y))**2)
    return f
def function4(coord): #Eggholder function f(512, 404.2319) = -959.6407
    x = coord[0]
    y = coord[1]
    f =(-(y + 47.0)*np.sin(np.sqrt(abs(x/2.0 + (y + 47.0))))- x * np.sin(np.sqrt(abs(x - (y + 47.0)))))
    return f


#--- MAIN ---------------------------------------------------------------------+

class Particle:
    def __init__(self,x0):
        self.position_i=[]          # particle position
        self.velocity_i=[]          # particle velocity
        self.pos_best_i=[]          # best position individual
        self.err_best_i=-1          # best error individual
        self.err_i=-1               # error individual

        for i in range(0,num_dimensions):
            self.velocity_i.append(random.uniform(-1,1))
            self.position_i.append(random.uniform(-1,1)*512)

    # evaluate current fitness
    def evaluate(self,costFunc):
        self.err_i=costFunc(self.position_i)

        # check to see if the current position is an individual best
        if self.err_i<self.err_best_i or self.err_best_i==-1:
            self.pos_best_i=self.position_i
            self.err_best_i=self.err_i
                    
    # update new particle velocity
    def update_velocity(self,pos_best_g):
        w=0.5       # constant inertia weight (how much to weigh the previous velocity)
        c1=1        # cognitive constant
        c2=2        # social constant
        
        for i in range(0,num_dimensions):
            r1=random.random()
            r2=random.random()
            
            vel_cognitive=c1*r1*(self.pos_best_i[i]-self.position_i[i])
            vel_social=c2*r2*(pos_best_g[i]-self.position_i[i])
            self.velocity_i[i]=w*self.velocity_i[i]+vel_cognitive+vel_social

    # update the particle position based off new velocity updates
    def update_position(self,bounds):
        for i in range(0,num_dimensions):
            self.position_i[i]=self.position_i[i]+self.velocity_i[i]
            
            # adjust maximum position if necessary
            if self.position_i[i]>bounds[i][1]:
                self.position_i[i]=bounds[i][1]

            # adjust minimum position if necessary
            if self.position_i[i]<bounds[i][0]:
                self.position_i[i]=bounds[i][0]
        
class PSO():
    def __init__(self,costFunc,x0,bounds,num_particles,maxiter):
        global num_dimensions

        num_dimensions=len(x0)
        err_best_g=-1                   # best error for group
        pos_best_g=[]                   # best position for group

        # establish the swarm
        swarm=[]
        for i in range(0,num_particles):
            swarm.append(Particle(x0))

        # begin optimization loop
        i=0
        while i<maxiter:
            #print i,err_best_g
            # cycle through particles in swarm and evaluate fitness
            for j in range(0,num_particles):
                swarm[j].evaluate(costFunc)

                # determine if current particle is the best (globally)
                if swarm[j].err_i<err_best_g or err_best_g==-1:
                    pos_best_g=list(swarm[j].position_i)
                    err_best_g=float(swarm[j].err_i)
            
            # cycle through swarm and update velocities and position
            for j in range(0,num_particles):
                swarm[j].update_velocity(pos_best_g)
                swarm[j].update_position(bounds)
            i+=1

        # print final results
        print("Best Solution: ", pos_best_g, " Value: ", err_best_g)


if __name__ == "__PSO__":
    main()

#--- RUN ----------------------------------------------------------------------+

               # initial starting location [x1,x2...]
import time

start = time.time()
print("STARTING PSO:")
bounds=[(-512,512),(-512,512)]
bounds1=[(-10,10),(-10,10)]
for i in range(10):
    initial= numpy.random.uniform(0,1,(2))*512
    PSO(function1,initial,bounds,num_particles=100,maxiter=500)
end = time.time()
print(end - start)
#--- END ----------------------------------------------------------------------+
