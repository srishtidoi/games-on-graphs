from simulation import Simulation
import random
import os
import sys

def main():
    population = int(sys.argv[1]) 
    average_degree = 4            
    num_episode = int(sys.argv[2])
    network_type = sys.argv[3]   
    learning_rule = sys.argv[4]

    simulation = Simulation(population, average_degree, network_type)
    
    for episode in range(num_episode):
        random.seed()
        simulation.one_episode(episode, rule = learning_rule)
        
        
if __name__ == '__main__':
    main()
