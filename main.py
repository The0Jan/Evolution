
import numpy as np
from random import choice 
from math import sqrt
import copy
from statistics import mean, pstdev
from os import remove

from evolutionary import Population, Person

# A quick model of an arrow being shoot at a wall and and pointing the cordinates it landed.  
def  shots_fired(shoot_xyz, archer_position = [0,0, -10],  G = 0.02 , W = 0.005 ):
        #archer position = (side length, height , distance from the wall)
    vel = copy.deepcopy(shoot_xyz)
    pos = archer_position
    for _ in range(30):
        pos = np.add(pos, vel) # Movement
        vel[1] = vel[1] - G     # Gravity for Y
        vel[0] = vel[0] + W     # Wind po X
        multiplied_vel = [element * 0.9 for element in vel]
        vel = multiplied_vel    # Air resistance
        if pos[2] <= 0:
            pos[2] = 0
            return pos
    return pos
    
# Checks how far did the arrow land from the apointed point on the wall. The smaller the fitness the better. 
def fitness(individual, aim = [3,3] ):
    opt = shots_fired(individual.value)

    return  sqrt( (opt[0] - aim[0])**2 + (opt[1] - aim[1])**2 ) + opt[2]*10

# Stores the maximal, minimal, and the mean and the standard deviation of every generation in an excel sheet
def store_statistics( fitnesses ):
    with open( 'statistics.csv', 'a' ) as f:
        fmax = max( fitnesses )
        fmin = min( fitnesses )
        fmean = mean( fitnesses )
        fstdev = pstdev( fitnesses, fmean )
        f.write( f'{fmax: 10.2f},{fmin: 10.2f},{fmean: 10.2f},{fstdev: 10.2f}\n' )

# Stores and signalizes every coming of a better individual
def store_best( best ):
    if best is not None:
        with open( 'best_solutions.csv', 'a' ) as f:
            x = best[0][0]
            y = best[0][1]
            z = best[0][2]
            fit = best[1]
            f.write( f'{x: 10.2f},{y: 10.2f},{z: 10.2f},{fit: 10.2f}\n' )

# Cleaner functions
def del_statistics():
    remove( 'statistics.csv' )
def del_best():
    remove( 'best_solutions.csv' )

# Evolves a created population by a given number of times and shows best outcomes
def test(generations,  population, mut_param, fitness, initiation_bounds = {"upper_bound":10 , "down_bound":0, "size": 3}):
    #In case of reapiting these two delete the last ones for the new ones to be created
    del_statistics()
    #del_best()
    populus = Population(population, initiation_bounds ,fitness,  mut_param)
    for _ in range(generations):
        store_statistics(populus.fitness_tabel())
        # Shows best and worst outcomes
        #print (populus.show_fittest(), populus.show_unfittest() )
        populus.evo()
        store_best(populus.update_best())



test(1000, 100, 0.001, fitness)

