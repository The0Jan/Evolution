

import numpy as np
from random import choice 
from math import sqrt
import copy
from statistics import mean, pstdev
from os import remove

# The class responsible for creating a single Person/Individual
class Person:
    # If no value is given, create a set of random values for the Person
    def __init__(self, initiation_bounds = {"upper_bound":3 , "down_bound":0, "size":3} , value = None):
        if value is None:
            self.value = []
            for _ in range(initiation_bounds["size"]):
                self.value.append(np.random.uniform(initiation_bounds["down_bound"],initiation_bounds["upper_bound"] )) # to do poprawy
        else:
            self.value = value
        self.bounds = initiation_bounds

    # Changes every value of a Person by a sample from a Gaussian distribution, while checking if the values ae in bounds
    def mutate(self, mutation_param):
        for i in range(len(self.value)):
            self.value[i] += np.random.normal(0, mutation_param)

            if self.value[i] < self.bounds['down_bound']:
                self.value[i] = self.bounds['down_bound']
            elif self.value[i] > self.bounds['upper_bound']:
                self.value[i] = self.bounds['upper_bound']


# The class responsible for the creation of a whole population based on the population _count
class Population:
    def __init__(self, population_count, initiation_bounds, fitness, mutation_parameter):
        self.mp = mutation_parameter            # Parameter used in the mutation process
        self.fitness = fitness                  # The algorithm for checking the fitness of an individual
        self.humanity = [Person(initiation_bounds) for number in range(0, population_count)] #The whole group of individuals
        self.humanity.sort(key=lambda a: self.fitness(a))   
        self.size = population_count
        self.best = [self.humanity[0].value, fitness(self.humanity[0])] # The best yet found sample/individual

# Show whenever a better individual is found
    def update_best(self):
        potential_best = self.fitness(self.humanity[0])
        if potential_best < self.best[1]:
            self.best = [self.humanity[0].value, potential_best]
            print(self.best)
            return self.best

# Creates a table of all fitnesses
    def fitness_tabel(self):
        fit_tab = []
        for i in range(self.size):
            fit_tab.append(self.fitness(self.humanity[i]))
        return fit_tab

# Shows the whole generation
    def show_pop(self):
        size = len(self.humanity)
        showcase = []
        for person in range(0,size):
            showcase.append([self.humanity[person].value, self.fitness(self.humanity[person])])
        print(showcase)

# Shows this generations best
    def show_fittest(self):
        return [self.humanity[0].value,self.fitness(self.humanity[0]) ]

# Shows this generations worst
    def show_unfittest(self):
        return [self.humanity[self.size-1].value,self.fitness(self.humanity[self.size-1]) ]

# Sorts the whole generation
    def sort_after_note(self):
        self.humanity.sort(key =lambda a:self.fitness(a))

# Tournament selection. Takes two individuals at random, the fitter wins. Reapets for the size of a generation.
    def tournament(self):
        winners = []
        for _ in range(self.size):
            competitor_1 = choice(self.humanity)
            competitor_2 = choice(self.humanity)
            if self.fitness(competitor_1) <= self.fitness(competitor_2):
                winners.append(competitor_1)
            else:
                winners.append(competitor_2)
        return winners

# Evolves a whole generation. Generation T becomes generation T+1
    def evo(self):
        new_gen =  self.tournament()
        for new_person in new_gen:
            new_person.mutate(self.mp)
        self.humanity = new_gen
        self.sort_after_note()
        



