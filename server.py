# server.py
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from model import bacServerModel, bacModel

from globals import *


def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Color": "red",
                 "Filled": "true",
                 "Layer": 0,
                 "r": 1,
                 "h": 1,
                 "w": 1}
    #if not agent.alive:
    if agent is None:
        portrayal["Shape"] = 'rect'
        portrayal['Color'] = 'green'
    if agent.mutated:
        portrayal["Color"] = 'blue'

    return portrayal


width_slider = UserSettableParameter('slider', "Initial X", WIDTH//2, 0, WIDTH, 1)
height_slider = UserSettableParameter('slider', "Initial Y", HEIGHT//2, 0, HEIGHT, 1)
initRad_slider = UserSettableParameter('slider', "Initialization Radius", RADIUS_INITIALIZATION, 0, 10, 1)
split_slider = UserSettableParameter('slider', "Probability of Splitting", SPLIT_CHANCE, 0, 1, 0.05)
mutation_slider = UserSettableParameter('slider', 'Probability of Mutation', MUTATION_RATE, 0, 1, 0.02)

grid = CanvasGrid(agent_portrayal, WIDTH, HEIGHT, 700, 700)
server = ModularServer(bacModel, 
                        [grid], 
                        "Eden Growth Model",
                        {"beginRad":initRad_slider, "splitChance":split_slider, "x":width_slider, "y":height_slider, 'mut_rate':mutation_slider})