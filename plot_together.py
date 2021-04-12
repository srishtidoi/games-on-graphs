import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import csv
import os
import sys
import random as rnd

dirs = ['scalefree_reputation_n100e100_','scalefree_reputation_n100e100_p0.7','scalefree_reputation_n100e100_p0.8','scalefree_reputation_n100e100_p0.95']

x_list = []
fc_list = []
fit_list = []
model_list = []
fit_x = np.linspace(0, 1, 100)

for d in dirs:
    os.chdir(d)
    all_files = os.listdir() # get list of all files in the working directory
    #print(all_files)
    all_files.remove('outputs')
    
    #n_eps = int(sys.argv[1]) # give the number of eps you want to plot
    #files = rnd.sample(all_files, n_eps) # pick n-eps number of eps at random
    files = all_files
    
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
        # Preparing x-values for log-log plot
        r_diff = np.array(0.02112 - x)
        

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
    #fit = np.poly1d(np.polyfit(x, fc, 1))
    model = sm.OLS(fc - 0.5, x).fit()

    plt.plot(x, fc, 'k-', linewidth=0.5, alpha=0.8)
    x_list.append(x)
    fc_list.append(fc)
    #fit_list.append(fit)
    model_list.append(model)
    os.chdir('..')

for model in model_list:
    
    #plt.scatter(x, fc, s=10, marker='D', facecolors='none', edgecolors='g', label = 'cooperators')
    plt.plot(fit_x,(0.5+model.predict(fit_x)))
    #plt.scatter(x, fd, s=10, marker='^', facecolors='none', edgecolors='r', label = 'defectors')
    #
    #plt.plot(x, fd, 'r--')
    plt.ylabel('Fraction of cooperators')
    plt.xlabel('r')
    plt.xlim([0,1])
    plt.ylim([0,1])
    #plt.axis([0, 0.07, 0, 1])
    #plt.xticks([0, 0.01, 0.02, 0.03])

plt.legend()
plt.show()

    # m, b = np.polyfit(r_diff, fc, 1)
    
    # plt.loglog(r_diff, fc, marker='D', linewidth='0')
    # plt.ylabel('Fraction of population')
    # ###plt.loglog(r_diff, m*r_diff+b)
    # plt.axis([0, 0.1, 0, 1])
    # plt.show()

