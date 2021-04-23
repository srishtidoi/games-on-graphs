import random as rnd
import numpy as np

class Agent:

    def __init__(self):
        self.point = 0.0    
        self.reputation = 0.05
        #self.tendency = rnd.random()
        self.strategy = None
        self.next_strategy = None
        self.strats = []
        self.stratpoints = []
        self.neighbors_id = [] # list of ids of all the neighbours of the focal agent

    def __imitate(self, agents, k_im):
        opp_id = rnd.choice(self.neighbors_id) # choose random opponent from neighbors
        opp = agents[opp_id] # agents = list of all agents
        transition_prob = 1/(1 + np.exp((self.point - opp.point)/k_im)) # transition probability

        # Imitate the strategy of a randomly picked neighbor with probablility = transition_prob
        if opp.strategy != self.strategy and rnd.random() < transition_prob:
            self.next_strategy = opp.strategy
        else:
            self.next_strategy = self.strategy

    def __bayesian(self, agents, k_by, p_max): 
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
            elif i<0:
                stop = True
            elif i>1:
                stop = True

        # update probabiities of all strats
        if stop == False:
            probability_diff = (2*p_max)/(1 + np.exp((avg_opp - self.point)/k_by)) - p_max
            #print(probability_diff)
            self.stratpoints[current_strat_id] += probability_diff
            self.stratpoints[other_strat_id] = 1 - self.stratpoints[current_strat_id]

        if rnd.random()<self.stratpoints[0]:
            self.next_strategy = self.strats[0]
        else:
            self.next_strategy = self.strats[1]

    
    def __reputation(self, agents, k_r1, k_r2, p): 
        ''' with fermi-like probability, imitate the neighbour with highest reputation (with probability p)
        or imitate a randomly chosen neighbour (with probability 1-p)'''

        if rnd.random()<p:
            neighbors = [agents[i] for i in self.neighbors_id]
            reps = [opp.reputation for opp in neighbors]
            max_rep = max(reps)
            max_index = reps.index(max_rep)
            max_opp = neighbors[max_index]
            
            transition_prob = 1/(1 + np.exp((self.reputation - max_rep)/k_r1)) # transition probability

            if max_opp.strategy != self.strategy and rnd.random() < transition_prob:
                self.next_strategy = max_opp.strategy
            else:
                self.next_strategy = self.strategy

        else:
            opp_id = rnd.choice(self.neighbors_id) # choose random opponent from neighbors
            opp = agents[opp_id] # agents = list of all agents
            transition_prob = 1/(1 + np.exp((self.point - opp.point)/k_r2)) # transition probability

            # Imitate the strategy of a randomly picked neighbor with probablility = transition_prob
            if opp.strategy != self.strategy and rnd.random() < transition_prob:
                self.next_strategy = opp.strategy
            else:
                self.next_strategy = self.strategy

                
        if self.next_strategy == 'C':
                self.reputation = (self.reputation)*(2 - self.reputation)
                
        
    def decide_next_strategy(self, agents, rule):
        ''' rule = learning rule (imitate, bayesian) '''

        #################################################################
        
        k_im = 0.1  # noise value for rule imitate
        k_by = 1.5  # noise parameter for rule bayesian
        k_r1 = 0.05  # noise paramter for rep-based imitation (rule reputation)
        k_r2 = 1  # noise paramter for payoff-based imitation (rule reputation)
        p_max = 0.1 # max probability difference for rule bayesian
        p = 0.3     # probability of choosinf rep-based imitation

        #################################################################

        if rule == "imitate":
            self.__imitate(agents, k_im)
        elif rule == "bayesian":
            self.__bayesian(agents, k_by, p_max)
        elif rule == "reputation":
            self.__reputation(agents, k_r1, k_r2, p)

    def update_strategy(self):
        self.strategy = self.next_strategy
