import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import csv
import os
import sys
import random as rnd

# list of directories with the phase diagrams
dirs = ['scalefree_reputation_n100e100_p0.0','scalefree_reputation_n100e100_p0.1','scalefree_reputation_n100e100_p0.2', 'scalefree_reputation_n100e100_p0.3','scalefree_reputation_n100e100_p0.4', 'scalefree_reputation_n100e100_p0.5', 'scalefree_reputation_n100e100_p0.7']

    #'smallworld_reputation_n100e100_p0.0','smallworld_reputation_n100e100_p0.3','smallworld_reputation_n100e100_p0.5', 'smallworld_reputation_n100e100_p0.6','smallworld_reputation_n100e100_p0.7', 'smallworld_reputation_n100e100_p0.9']

    #

    #'scalefree_bayesian_n100e20_p0.05','scalefree_bayesian_n100e20_p0.1','scalefree_bayesian_n100e20_p0.2', 'scalefree_bayesian_n100e20_p0.3'] #, 'scalefree_bayesian_n100e20_p0.8']

    #'lattice_reputation_n100e100_', 'lattice_reputation_n100e100_p0.7', 'lattice_reputation_n100e100_p0.9']

    #'smallworld_reputation_n100e100_p0.3','smallworld_reputation_n100e100_p0.5', 'smallworld_reputation_n100e100_p0.6', 'smallworld_reputation_n100e100_p0.7', 'smallworld_reputation_n100e100_p0.8','smallworld_reputation_n100e100_p0.9', 'smallworld_reputation_n100e100_p0.95']


    #'scalefree_reputation_n100e100_p0.5','scalefree_reputation_n100e100_p0.7','scalefree_reputation_n100e100_p0.8','scalefree_reputation_n100e100_p0.95']

# list of p values 
legend = ['p = 0', 'p = 0.1', 'p = 0.2', 'p = 0.3', 'p = 0.4', 'p = 0.5', 'p = 0.7']

x_list = []
fc_list = []
fit_list = []
model_list = []

# x values for the fit
fit_x = np.linspace(0, 1, 100)

for d in dirs:
    os.chdir(d)
    files = os.listdir() # get list of all files in the working directory
    #print(all_files)
    files.remove('outputs')
        
    # preparing x-values (values of r)
    x = []
    with open('phase_diagram0.csv', 'r') as forx:
        xreader = csv.reader(forx)
        cols = next(xreader) # column headings out of the way
        
        rows = []
        for row in xreader:
            rows.append(row)
            
        for row in rows:
            x.append(float(row[1]))
            #print(row[1])
        
        x = np.array(x)
        
    # looping over all files for y values
    fc = np.zeros(len(x))
    for filename in files:
        rows = []
        cols = []
            
        with open(filename, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            cols = next(csvreader) # column headings out of the way
            
            for row in csvreader:
                rows.append(row)
        
            # Preparing y-values for fc plot 
            y_temp = np.empty(0) # value for current episode (file)
            for row in rows:
                y_temp = np.append(y_temp, float(row[2]))

            #print('y_temp = ', y_temp)
            fc += y_temp # sum of all fcs over all the episodes
            #print('fc = ',fc)
        

    print('fc = ', fc)

    fc = fc/len(files) # taking average over all episodes
    fd = 1 - fc # fraction of defectors


    ### fitting
    
    #fit = np.poly1d(np.polyfit(x, fc, 3))      # polynomial fit
    #model = sm.OLS(fc - 0.5, x).fit()         # linear fit with fixed intercept
    #plt.plot(x, fc, 'k-', linewidth=0.5, alpha=0.7)
    
    ### if no fit is needed
    
    legend_label = legend[dirs.index(d)]      
    plt.plot(x, fc, linewidth=0.7, label=legend_label)
    
    x_list.append(x)
    fc_list.append(fc)
    #fit_list.append(fit)
    #model_list.append(model)
    os.chdir('..')

# plotting all the fits 
#for fit in fit_list:

    ### legends
    #legend_label = legend[model_list.index(model)]
    #legend_label = legend[fit_list.index(fit)]

    ### plots
    #plt.plot(fit_x,(0.5+model.predict(fit_x)), label=legend_label)
    #plt.plot(fit_x,fit(fit_x), label=legend_label, linewidth=1)

    #plt.ylabel('Fraction of cooperators')
    #plt.xlabel('r')
    #plt.xlim([0,0.5])
    #plt.ylim([0,1])
    

plt.ylabel('Fraction of cooperators')
plt.xlabel('r')
plt.xlim([0,0.5])
plt.ylim([0,1])

plt.legend()
plt.show()

    
