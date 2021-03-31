import numpy as np
import random as rnd
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import os
from agents import Agent



class Simulation:

    def __init__(self, population, average_degree, network_type):

        self.network_type = network_type
        self.network = None
        self.agents = self.__generate_agents(population, average_degree)
        self.initial_cooperators = self.__choose_initial_cooperators()
        self.population = population

    def __generate_agents(self, population, average_degree):
        ''' generate the network and add neighbors to every agent/node '''
        if self.network_type == 'lattice':
            self.network = self.__generate_lattice(population)

        elif self.network_type == 'RR':
            self.network = nx.random_regular_graph(average_degree, population)

        elif self.network_type == 'smallworld':
            self.network = nx.watts_strogatz_graph(population, average_degree, 0.3)

        elif self.network_type == 'scalefree':
            self.network = nx.barabasi_albert_graph(population, average_degree)

        agents = [Agent() for id in range(population)]
            

        if self.network_type == 'lattice': # node id for lattice is of the form (x,y)
            n = int(np.sqrt(population))
            for index, focal in enumerate(agents): # index of an agent can be translated to node id on the graph
                neighbors_id = list(self.network[int(index//n), int(index%n)]) #sq brackets give the neighbors/adjacent nodes for the given node
                for (x,y) in neighbors_id:
                    nb_id = int(x*n+y)
                    focal.neighbors_id.append(nb_id) # attribute of agent class

        else:
            for index, focal in enumerate(agents) :
                neighbors_id = list(self.network[index])
                for nb_id in neighbors_id:
                    focal.neighbors_id.append(nb_id)
                    
        return agents

    def __generate_lattice(self, population):
        ''' generate lattice with degree 4 (can modify to make it degree 8) '''
        n = int(np.sqrt(population))
        G = nx.grid_graph(dim = [n,n])
        return G

    def __choose_initial_cooperators(self): # for imitate rule only
        ''' choose the initial cooperators (modify initial fraction of cooperators here)'''

        population = len(self.agents)
        fraction_coop = 1/2 # setting initial fc  
        self.initial_cooperators = rnd.sample(range(population), k = int(population*fraction_coop)) #randomly choosing a fraction of the population to be cooperators

    def __initialize_strategy(self, rule):
        ''' assign initial strategies to agents '''

        # define strategies for each agent (used for bayesian)
        for agent in self.agents:
            agent.strats = ['C', 'D']
            agent.stratpoints = [0.5, 0.5] # initial points for bayesian rule

        if rule == 'imitate':
            for index, focal in enumerate(self.agents):
                if index in self.initial_cooperators:
                    focal.strategy = 'C' # Cooperators
                else :
                    focal.strategy = 'D' # Defectors

        elif rule == 'bayesian':
            for focal in self.agents:
                focal.strategy = rnd.choice(focal.strats)
                
    def __count_payoff(self, r):
        R = 1     # Reward
        S = -r    # Sucker
        T = 1+r   # Temptation
        P = 0     # Punishment

        for focal in self.agents:
            focal.point = 0.0
            for nb_id in focal.neighbors_id:
                neighbor = self.agents[nb_id]
                if focal.strategy == 'C' and neighbor.strategy == 'C':
                    focal.point += R
                elif focal.strategy == "C" and neighbor.strategy == "D":   
                    focal.point += S
                elif focal.strategy == "D" and neighbor.strategy == "C":   
                    focal.point += T
                elif focal.strategy == "D" and neighbor.strategy == "D":  
                    focal.point += P

    def __update_strategy(self, rule):
        if rule == 'imitate':
            focal = rnd.choice(self.agents)
            focal.decide_next_strategy(self.agents, rule = rule)
            focal.update_strategy()

        if rule == 'bayesian':
            for focal in self.agents:
                focal.decide_next_strategy(self.agents, rule = rule)
                focal.update_strategy()

    def __count_fc(self):
        ''' calculate the fraction of cooperative agents '''

        fc = len([agent for agent in self.agents if agent.strategy == 'C'])/len(self.agents)

        return fc

    def __play_game(self, episode, r, rule):
        ''' continue game untill fc converges '''

        tmax = 1000000
        tc = 10000 # t after which convergence condition is checked
        tavg = 100 # t over which avg is taken to check convergence

        self.__initialize_strategy(rule = rule)
        initial_fc = self.__count_fc()
        fc_hist = [initial_fc]
        print(f"Episode:{episode}, r:{r:.4f}, Time: 0, fc:{initial_fc:.3f}")

        for t in range(1, tmax+1):
            self.__count_payoff(r)
            self.__update_strategy(rule = rule) # rule = imitate, bayesian
            fc = self.__count_fc()
            fc_hist.append(fc)
            print(f"Episode:{episode}, r:{r:.4f}, Time:{t}, fc:{fc:.3f}")

            # Convergence conditions
            if fc == 0 or fc == 1:
                fc_converged = fc
                comment = "fc 0 or 1"
                break
            
            if t >= tc and np.absolute(np.mean(fc_hist[t-tavg:t-1]) - fc)/fc < 0.0001:
                fc_converged = np.mean(fc_hist[t-tavg:t])
                comment = "fc converged"
                break

            if t == tmax:
                fc_converged = np.mean(fc_hist[t-tavg:t])
                comment = "fc (final timestep)"
                break

        print(f"r:{r:.4f}, Time:{t}, {comment}:{fc_converged:.3f}")

        return fc_converged

    def one_episode(self, episode, rule):
        ''' run one episode'''

        result = pd.DataFrame({'r': [], 'fc': []})

        if rule == 'imitate':
            self.__choose_initial_cooperators()


        ### choose the range of r values here
        
        # n1 = np.arange(0,0.02, 0.002)
        # n2 = np.arange(0.02, 0.022, 0.0004)
        # n3 = np.arange(0.022, 0.032, 0.002)
        # r_range = np.append(n1, n2)
        # r_range = np.append(r_range, n3)

        r_range = np.arange(0, 0.008, 0.004)
        for r in r_range:
            fc_converged = self.__play_game(episode, r, rule = rule)
            new_result = pd.DataFrame([[format(r, '.4f'), fc_converged]], columns = ['r', 'fc'])
            result = result.append(new_result)
    
        result.to_csv(f"phase_diagram{episode}.csv")
        
