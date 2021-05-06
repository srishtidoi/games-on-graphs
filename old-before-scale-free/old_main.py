from simulation import Simulation
import random
import os

def main():
    population = 25              # Agent number
    average_degree = 4            # Average degree of network
    num_episode = 3              # Number of episodes for taking ensemble average
    network_type = 'lattice'   # Topology of network
    learning_rule = 'imitate'

    # Creating new directory for data files
    new_dirname = "phase_diagrams_n"+str(population)+"e"+str(num_episode)+"_"+network_type+"_"+learning_rule+'_test'

    os.mkdir(new_dirname)
    os.chdir(new_dirname)

    print(new_dirname)
    simulation = Simulation(population, average_degree, network_type)
    
    for episode in range(num_episode):
        random.seed()
        simulation.one_episode(episode, rule = learning_rule)
        
        
if __name__ == '__main__':
    main()
