from vsimulation import vSimulation
import random
import os

def main():
    population = 2500        # Agent number
    average_degree = 4         # Average degree of network
    num_episode = 1            # Number of episodes for taking ensemble average.
    
    ## It doesn't make sense to take ensemble average here because every episode will have a different numebr of timesteps and fc will go to zero in some eps faster than it will in others. So the average will end up looking weird near the fc=0 axis.

    network_type = 'smallworld'   # Topology of network

    # Creating new directory for data files
    new_dirname = "vol_phase_diagrams_n"+str(population)+"e"+str(num_episode)+"_"+network_type
    os.mkdir(new_dirname)
    os.chdir(new_dirname)
    simulation = vSimulation(population, average_degree, network_type)

    for episode in range(num_episode):
        random.seed()
        simulation.one_episode(episode)

if __name__ == '__main__':
    main()
