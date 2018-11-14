#model.py

#Library Imports
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import random

#Supporting Script Imports
from globals import *

if RAND_SEED >= 0:
    random.seed(RAND_SEED)

class bacAgent(Agent):
    '''Agent for Eden Growth Model Simulation'''
    def __init__(self, unique_id, model, mutated = False, split_rate=SPLIT_CHANCE, mut_rate=MUTATION_RATE):
        super().__init__(unique_id, model)

        #additional variable initialization can go here
        self.mut_rate = MUTATION_RATE
        self.mut_effect = MUTATION_EFFECT
        self.prob_split = split_rate
        self.mutated = mutated
        #
        #

    def step(self):
        #agent step behavior goes here
        roll = random.random()
        # if roll < self.mut_rate:
        #     self.mutated = True
        if roll < self.prob_split:
            self.split()


    def split(self):
        typ = NHOOD_TYPE
        if NHOOD_TYPE == 'Moore':
            mBool = True
        elif NHOOD_TYPE == 'Neumann':
            mBool = False
        else:
            print('Error: Invalid values for NHOOD_TYPE. Allowable values are "Moore" and "Neumann".')
            return

        #get possible areas to add agent
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=mBool, include_center=False) #radius argument allows for larger search area
        
        #Make sure cell is unoccupied
        occupied = True
        ctr = 0
        while occupied:
            ctr += 1
            occupied = False

            new_position = random.choice(possible_steps)
            possible_steps.remove(new_position)
            contents = self.model.grid.get_cell_list_contents([new_position])

            if len(contents) >= 1:
                occupied = True
            if len(possible_steps) == 0 and occupied:
                return

        #if we get here there's an unoccupied space next to this agent
        #so we'll spawn an agent in that location
        a = bacAgent(self.model.num_agents, self.model, self.mutated, self.mut_rate)
        roll = random.random()
        if roll < a.mut_rate:
            a.mutated = not self.mutated
        self.model.schedule.add(a)
        self.model.grid.place_agent(a, new_position)
        self.model.num_agents += 1

class bacModel(Model):
    '''world model for Eden Growth Model Simulation'''
    def __init__(self, beginRad, splitChance, x=-1, y=-1, mut_rate=MUTATION_RATE):
        self.running = True
        self.num_agents = 0
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(WIDTH, HEIGHT, IS_TOROIDAL) #True for toroidal
        #self.datacollector = DataCollector(
        #    model_reporters = {"Identifier": function_name}, #note no parentheses, just function name
        #    agent_reporter = {"Identifier2": function_name2})

        if x == -1:
            x = self.grid.width // 2
        if y == -1:
            y = self.grid.height // 2

        #create subsequent agents
        positions = self.grid.get_neighborhood((x,y), moore=False, radius=beginRad, include_center=True)
        for coord in positions:
            roll = random.random()
            a = bacAgent(self.num_agents, self, False, splitChance)
            self.num_agents += 1
            self.schedule.add(a)
            self.grid.place_agent(a, coord)


    def step(self):
        #self.datacollector.collect(self)
        self.schedule.step()

# def ExampleDataCollectorFunction():
#     exampleOperations()


########################
###Deprecated Classes###
########################

class bacServerModel(Model):
    ################
    ###Deprecated###
    ################
    def __init__(self, width, height, beginRad):
            self.running = True
            self.num_agents = width * height
            self.schedule = RandomActivation(self)
            self.grid = MultiGrid(width, height, IS_TOROIDAL) #True for toroidal
            #self.datacollector = DataCollector(
            #    model_reporters = {"Identifier": function_name}, #note no parentheses, just function name
            #    agent_reporter = {"Identifier2": function_name2})

            for x in range(self.grid.width):
                for y in range(self.grid.height):
                    a = bacServerAgent(self.num_agents, self)
                    self.num_agents += 1
                    self.schedule.add(a)
                    self.grid.place_agent(a, (x,y))

            x = self.grid.width // 2
            y = self.grid.height // 2

            #create subsequent agents
            positions = self.grid.get_neighborhood((x,y), moore=False, radius=beginRad, include_center=True)
            for coord in positions:
                ag = self.grid.get_cell_list_contents([coord])[0]
                ag.activate()


    def step(self):
        #self.datacollector.collect(self)
        self.schedule.step()


class bacServerAgent(bacAgent):
    ################
    ###Deprecated###
    ################
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.alive = False

    def activate(self):
        self.alive = True


    def split(self):
        if not self.alive:
            return

        typ = NHOOD_TYPE
        if NHOOD_TYPE == 'Moore':
            mBool = True
        elif NHOOD_TYPE == 'Neumann':
            mBool = False
        else:
            print('Error: Invalid values for NHOOD_TYPE. Allowable values are "Moore" and "Neumann".')
            return

        #get possible areas to add agent
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=mBool, include_center=False) #radius argument allows for larger search area
        
        #Make sure cell is unoccupied
        occupied = True
        ctr = 0
        while occupied:
            ctr += 1
            occupied = False

            new_position = random.choice(possible_steps)
            possible_steps.remove(new_position)
            contents = self.model.grid.get_cell_list_contents([new_position])

            if contents[0].alive:
                occupied = True
            if len(possible_steps) == 0 and occupied:
                return

        a = self.model.grid.get_cell_list_contents([new_position])[0]
        a.activate()





