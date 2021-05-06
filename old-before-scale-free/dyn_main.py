from dynamics import Dynamics
import random
import os

def main():
    population = 6400          # Number of agents
    average_degree = 4         # Average degree of network
    num_episode = 1            # Number of episodes for taking ensemble average
    network_type = 'lattice'   # Topology of network

    # Creating new directory for data files
    new_dirname = "dyn_time_evolution_n"+str(population)+"e"+str(num_episode)+"_"+network_type
    os.mkdir(new_dirname)
    os.chdir(new_dirname)
    simulation = Dynamics(population, average_degree, network_type)

    for episode in range(num_episode):
        random.seed()
        simulation.one_episode(episode)

if __name__ == '__main__':
    main()
