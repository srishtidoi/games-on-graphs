import numpy as np
import random as rnd
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from agents import Agent
import os


class vSimulation:

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
            self.network = nx.watts_strogatz_graph(population, average_degree, 0.5)

        agents = [Agent() for id in range(population)]

        if self.network_type == 'lattice':
            n = int(np.sqrt(population))
            for index, focal in enumerate(agents):
                neighbors_id = list(self.network[int(index//n), int(index%n)])
                #sq brackets give the neighbors/adjacent nodes for the given node
                for (x,y) in neighbors_id:
                    nb_id = int(x*n+y)
                    focal.neighbors_id.append(nb_id) #attribute of agent class

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

    def __choose_initial_cooperators(self):
        ''' choose the initial cooperators (modify initial fc here)'''

        population = len(self.agents)

        self.initial_cooperators = rnd.sample(range(population), k = int(population/3)) #randomly choosing a third of the population to be cooperators

            
    def __initialize_strategy(self):
        ''' assign initial strategies to agents '''
        
        population = len(self.agents)
        rest_population = []
        for index, focal in enumerate(self.agents):
            if index in self.initial_cooperators:
                focal.strategy = 'C'
            elif rnd.random() < 0.5: # randomly choosing half the remaining agents to be loners            
                focal.strategy = 'L'
            else:
                focal.strategy = 'D'

    def __count_payoff(self, r): # Payoff for loners is a constant s (P<s<R)
        ''' count '''
        
        R = 1     # Reward
        S = -r    # Sucker
        T = 1+r   # Temptation
        P = 0     # Punishment

        for focal in self.agents:
            focal.point = 0.0
            for nb_id in focal.neighbors_id:
                neighbor = self.agents[nb_id]
                if focal.strategy == 'L':
                    focal.point = 0.3
                elif neighbor.strategy == 'L':
                    focal.point = 0.3
                elif focal.strategy == 'C' and neighbor.strategy == 'C':
                    focal.point +=R
                elif focal.strategy == "C" and neighbor.strategy == "D":   
                    focal.point += S
                elif focal.strategy == "D" and neighbor.strategy == "C":   
                    focal.point += T
                elif focal.strategy == "D" and neighbor.strategy == "D":  
                    focal.point += P

    def __update_strategy(self, rule = 'glauber'):
        focal = rnd.choice(self.agents)
        focal.decide_next_strategy(self.agents, rule = rule)
        focal.update_strategy()

    def __count_fc(self):
        ''' calculate the fraction of cooperative agents '''

        fc = len([agent for agent in self.agents if agent.strategy == 'C'])/len(self.agents)

        return fc

    def __count_fl(self):
        ''' calculate the fraction of loners '''

        fl = len([agent for agent in self.agents if agent.strategy == 'L'])/len(self.agents)

        return fl
    
    def __play_game(self, episode, r):
        ''' continue game untill fc converges '''

        tmax = 10000000

        self.__initialize_strategy()
        initial_fc = self.__count_fc()
        initial_fl = self.__count_fl()
        fc_hist = [initial_fc]
        fl_hist = [initial_fl]
        
        print(f"Episode:{episode}, r:{r:.4f}, Time: 0, fc:{initial_fc:.3f}, fl:{initial_fl:.3f}")

        for t in range(1, tmax+1):
            self.__count_payoff(r)
            self.__update_strategy(rule = 'glauber')
            fc = self.__count_fc()
            fl = self.__count_fl()
            fc_hist.append(fc)
            fl_hist.append(fl)
            
            print(f"Episode:{episode}, r:{r:.4f}, Time:{t}, fc:{fc:.3f}, fl:{fl:.3f}")

            # Convergence conditions
            if (fc == 0 or fc == 1) and (fl == 0 or fl ==1):
                fc_converged = fc
                fl_converged = fl
                comment = "fc 0 or 1"
                break
            
            if t >= 100000 and np.absolute(np.mean(fc_hist[t-1000:t-1]) - fc)/fc < 0.001:
                fc_converged = np.mean(fc_hist[t-1000:t])
                fl_converged = np.mean(fl_hist[t-1000:t])
                comment = "fc and fl converged"
                break

            if t == tmax:
                fc_converged = np.mean(fc_hist[t-1000:t])
                fl_converged = np.mean(fl_hist[t-1000:t])
                comment = "(final timestep)"
                break

        print(f"r:{r:.4f}, Time:{t}, {comment}:{fc_converged:.3f}, {fl_converged:.3f}")

        return [fc_converged, fl_converged]

    def one_episode(self, episode):
        ''' run one episode'''

        result = pd.DataFrame({'r': [], 'fc': [], 'fl': []})
        self.__choose_initial_cooperators()

        for r in np.arange(0, 0.5, 0.01):
            converged = self.__play_game(episode, r)
            fc_converged = converged[0]
            fl_converged = converged[1]
            new_result = pd.DataFrame([[format(r, '.4f'), fc_converged, fl_converged]], columns = ['r', 'fc', 'fl'])
            result = result.append(new_result)
    
        result.to_csv(f"phase_diagram{episode}.csv")
