############################################
## Global Parameters for Eden Growth Model##
############################################


#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-#
#-Model Initialization Parameters-#
#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-#
RADIUS_INITIALIZATION = 0 #one agent is spawned automatically at the center
                          #This controls the size of the initial colony
                          #value of N means that every space N spaces away from the center will contain an agent at initialization
IS_TOROIDAL = False
MUTATION_RATE = 0.1
MUTATION_EFFECT = 0
WIDTH = 100
HEIGHT = 100
#RADIUS = 1
SPLIT_CHANCE = 0.5 #range from 0 to 1, continuous. 1 = 100% chance of splitting, 0 = 0% chance
NHOOD_TYPE = 'Moore' #'Moore' or 'Neumann'. Moore includes diagonals.
RAND_SEED = -1 #put a positive number to seed with a specific number


#-+-+-+-+-+-+-+-+-+-+-#
#-Runtime  Parameters-#
#-+-+-+-+-+-+-+-+-+-+-#
NUM_STEPS = -1 #-1 for infinite loop (!!CAUTION!!)
SERVER = True
SERVER_PORT = 8521
SERVER_MAXHEIGHT = 100
SERVER_MAXWIDTH = 100