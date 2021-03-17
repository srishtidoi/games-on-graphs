import random as rnd
import numpy as np

class Agent:

    def __init__(self):
        self.point = 0.0    
        self.strategy = None
        self.next_strategy = None
        self.strats = []
        self.stratpoints = []
        self.neighbors_id = [] # list of ids of all the neighbours of the focal agent

    def __imitate(self, agents): # update rule imitation
        opp_id = rnd.choice(self.neighbors_id) # choose random opponent from neighbors
        opp = agents[opp_id] # agents = list of all agents
        k = 0.1 # noise parameter
        transition_prob = 1/(1 + np.exp((self.point - opp.point)/k)) # transition probability

        # Imitate the strategy of a randomly picked neighbor with probablility = transition_prob
        if opp.strategy != self.strategy and rnd.random() < transition_prob:
            self.next_strategy = opp.strategy
        else:
            self.next_strategy = self.strategy

    def __bayesian(self, agents): # update rule bayesian
        avg_opp = 0 # average payoff of all nrighbours
        number_opps = len(self.neighbors_id) # number of neighbors

        # current strat and other strat id 
        current_strat_id = self.strats.index(self.strategy) 
        other_strat = [x for x in self.strats if x != self.strategy] 
        other_strat_id = self.strats.index(other_strat[0]) 
        
        for agent_id in self.neighbors_id: # iterate over all neighbors
            opp = agents[agent_id]
            avg_opp += opp.point

        avg_opp = avg_opp/number_opps
        
        stop = False # signal to stop if either strategy reaches prob 1
        for i in self.stratpoints:
            if abs(i-1) < 0.0001:
                stop = True

        # update probabiities of all strats
        k = 1.5 # noise parameter
        if stop == False:
            probability_diff = 0.2/(1 + np.exp((avg_opp - self.point)/k)) - 0.1
            #print(probability_diff)
            self.stratpoints[current_strat_id] += probability_diff
            self.stratpoints[other_strat_id] = 1 - self.stratpoints[current_strat_id]

        self.next_strategy = self.strats[self.stratpoints.index(max(self.stratpoints))]

    def decide_next_strategy(self, agents, rule):
        ''' rule = learning rule (imitate, bayesian) '''
        if rule == "imitate":
            self.__imitate(agents)
        elif rule == "bayesian":
            self.__bayesian(agents)

    def update_strategy(self):
        self.strategy = self.next_strategy
