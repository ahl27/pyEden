#run.py

#Library Imports
import numpy as np
import matplotlib.pyplot as plt
from time import sleep

#Supporting Script imports
from globals import *
from model import bacModel, bacServerModel
from server import server

if RAND_SEED >= 0:
    np.random.seed(RAND_SEED)
graphs = []

def main():
    
    if SERVER:
        server.port = SERVER_PORT
        server.launch()

    elif NUM_STEPS >= 0:
        model = bacModel(WIDTH, HEIGHT, RADIUS_INITIALIZATION)
        quit = graph(model, 0)
        for i in range(NUM_STEPS):
            model.step()
            quit = graph(model, i+1)
            if quit:
                break

    else: #-1 indicates infinite loop
        model = bacModel(WIDTH, HEIGHT, RADIUS_INITIALIZATION)
        i = 0
        quit = graph(model, i)
        while True:
            model.step()
            i += 1
            quit = graph(model, i)
            if quit:
                break

    #get data from datacollector, returned as a pandas dataframe
    #modelParameters = model.datacollector.get_model_vars_dataframe()
    #agentParameters = model.datacollector.get_agent_vars_dataframe()



def graph(model, gen):
    at_least_one_unoccupied = False
    agent_counts = np.zeros((model.grid.width, model.grid.height))
    for cell in model.grid.coord_iter():
        cell_content, x, y = cell
        agent_count = len(cell_content)
        agent_counts[x][y] = agent_count
        if agent_count == 0:
            at_least_one_unoccupied = True
    plt.imshow(agent_counts, interpolation='nearest')
    plt.colorbar()
    plt.title('Generation: ' + str(gen))
    plt.show()
    return not at_least_one_unoccupied



if __name__ == '__main__':
    main()