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
            self.network = nx.watts_strogatz_graph(population, average_degree, 0.6)

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

    def __choose_initial_cooperators(self): # for imitate and repuation rules only
        ''' choose the initial cooperators (modify initial fraction of cooperators here)'''

        population = len(self.agents)
        fraction_coop = 1/2 # setting initial fc  
        self.initial_cooperators = rnd.sample(range(population), k = int(population*fraction_coop)) #randomly choosing a fraction of the population to be cooperators

    def __initialize_strategy(self, rule):
        ''' assign initial strategies to agents '''

        # define strategies for each agent (used for bayesian)
        for agent in self.agents:
            agent.reputation = 0.0 # initial reputation for reputation rule
            agent.strats = ['C', 'D']
            agent.stratpoints = [0.5, 0.5] # initial points for bayesian rule
            
        if rule == 'imitate' or rule == 'reputation':
            for index, focal in enumerate(self.agents):
                if index in self.initial_cooperators:
                    focal.strategy = 'C' # Cooperators
                else :
                    focal.strategy = 'D' # Defectors

        elif rule == 'bayesian' or rule == 'bayesian2':
            for focal in self.agents:
                focal.strategy = rnd.choice(focal.strats)
                
    def __count_payoff(self, r, game):

        if game=="PD":
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

        if game=="OPDYN":
            for focal in self.agents:
                focal.point = 0.0
                for nb_id in focal.neighbors_id:
                    neighbor = self.agents[nb_id]
                    if focal.strategy == neighbor.strategy:
                        focal.point += 1
                    else:
                        focal.point += -r

        if game=="PGD":
            # resetting all points to 0
            for focal in self.agents:
                focal.point = 0.0

            for focal in self.agents:
                N = len(focal.neighbors_id)
                cooperators = []
                defectors = []

                # iterating over all neighbours and classifying them as C or D
                for nb_id in focal.neighbors_id:
                    neighbor = self.agents[nb_id]
                    if neighbor.strategy == "C":
                        cooperators.append(neighbor)
                    else:
                        defectors.append(neighbor)
                # classifying focal as C or D
                if focal.strategy == "C":
                    cooperators.append(focal)
                else:
                    defectors.append(focal)

                # adding payoffs to pre-existing points
                for agent in cooperators:
                    agent.point += (len(cooperators)*r/N+1) - 1
                for agent in defectors:
                    agent.point += (len(cooperators)*r/N+1)

    def __update_strategy(self, rule, fc, fr, p_c):
        if rule == 'imitate' or rule == 'reputation':
            focal = rnd.choice(self.agents)
            focal.decide_next_strategy(self.agents, rule = rule, fc=fc, fr=fr, p_c = p_c)
            focal.update_strategy()
                       
        if rule == 'bayesian' or rule == 'bayesian2':
            for focal in self.agents:
                focal.decide_next_strategy(self.agents, rule = rule, fc=fc, fr=fr, p_c=p_c)
                focal.update_strategy()

    def __count_fc(self):
        ''' calculate the fraction of cooperative agents '''

        fc = len([agent for agent in self.agents if agent.strategy == 'C'])/len(self.agents)

        return fc

    def __count_fr(self, game):
        ''' calculate the fraction of agents that have reputation above 0.9'''

        if game=="PD" or game=="PGD":
            reps = [focal.reputation for focal in self.agents]
            bigreps = [x for x in reps if x>0.9]
            fr = len(bigreps)/len(reps)
        elif game=="OPDYN":
            reps = [focal.reputation for focal in self.agents]
            bigreps_p = [x for x in reps if x>0.9]
            bigreps_n = [x for x in reps if x<-0.9]
            frp = len(bigreps_p)/len(reps)
            frn = len(bigreps_n)/len(reps)
            fr = [frp, frn]

        return fr

    def __play_game(self, episode, r, rule, output):
        ''' continue game untill fc converges '''

        if rule == 'bayesian' or rule == 'bayesian2':
            tmax = 1000000
            tc = 10000 # t after which convergence condition is checked
            tavg = 100 # t over which avg is taken to check convergence

        elif rule == 'imitate' or rule == 'reputation':
            tmax = 100000000
            tc = 1000000
            tavg = 5000
            
        self.__initialize_strategy(rule = rule)
        initial_fc = self.__count_fc()
        fc_hist = [initial_fc]
        print(f"Episode:{episode}, r:{r:.4f}, Time: 0, fc:{initial_fc:.3f}")

        if output == 'rep':        
            rep_result = pd.DataFrame({'timestep': [], 'reputation': []})
            rep_result = self.__take_snapshot(0, episode, rep_result)
            timeseries = pd.DataFrame({'r': [], 't': [], 'fc': []})
        
        fc = initial_fc
        #print(fc)
        for t in range(1, tmax+1):
            self.__count_payoff(r, game="PD")
            fr = self.__count_fr(game="PD")
            self.__update_strategy(rule = rule, fc=fc, fr=fr, p_c=r) # rule = imitate, bayesian, reputation
            
            fc = self.__count_fc()
            fc_hist.append(fc)
                        
            # take a snapshot every 10th timestep
            if output == 'rep':
                if t%10 == 0:
                    rep_result = self.__take_snapshot(t, episode, rep_result)
                new_time = pd.DataFrame([[format(r, '.4f'), t, fc]], columns = ['r', 't', 'fc'])
                timeseries = timeseries.append(new_time)
            
                
            print(f"Episode:{episode}, r:{r:.4f}, Time:{t}, fc:{fc:.3f}")

            # Convergence conditions
            if fc == 0 or fc == 1:
                fc_converged = fc
                comment = "fc 0 or 1"
                break
            
            if t >= tc and np.absolute(np.mean(fc_hist[t-tavg:t-1]) - fc)/fc < 0.01:
                fc_converged = np.mean(fc_hist[t-tavg:t])
                comment = "fc converged"
                break

            if t == tmax:
                fc_converged = np.mean(fc_hist[t-tavg:t])
                comment = "fc (final timestep)"
                break

        print(f"r:{r:.4f}, Time:{t}, {comment}:{fc_converged:.3f}")
        if output == 'rep':
            rep_result.to_pickle(f"reputation_evol{episode}.pkl")
            timeseries.to_csv(f"timeseries{episode}.csv")
        
        return fc_converged

    def __take_snapshot(self, timestep, episode, rep_result):
        # time evolution plot 
        val_map = {}
        for index, focal in enumerate(self.agents):
            val_map[index] = focal.reputation

        values = list(val_map.values())
        #values = [val_map.get(node) for node in self.network.nodes()]
        new_rep_result = pd.DataFrame([[timestep, values]], columns = ['timestep', 'reputation'])
        rep_result = rep_result.append(new_rep_result)
        return rep_result
        
    def one_episode(self, episode, rule, output):
        ''' run one episode'''

        result = pd.DataFrame({'r': [], 'fc': []})
        

        if rule == 'imitate' or rule == 'reputation':
            self.__choose_initial_cooperators()

        ####################################################################
        
        if output == 'null': # range of values for regular sim
            r_range = np.arange(0, 0.05, 0.001)
        elif output == 'rep': # value of r for sim with rep output
            r_range = [0.9]

        ####################################################################
        
        for r in r_range:
            fc_converged = self.__play_game(episode, r, rule = rule, output=output)
            new_result = pd.DataFrame([[format(r, '.4f'), fc_converged]], columns = ['r', 'fc'])
            result = result.append(new_result)
    
        result.to_csv(f"phase_diagram{episode}.csv")
        
