################################################################################
#
# To plot multiple simulations in the same figure. Give the list of files as
# dirs and the labels as the legend.the plot title and limts can be specified.
#
# Run from outside the target directories.
#
################################################################################
################################################################################

dirs = ['scalefree_reputation_n100e100_p0.3', 'scalefree_reputation_n100e100_fr_p0.3']
legend = ['without $f_{R}$', 'with $f_{R}$']
plot_title = 'Network: Scalefree, Model: Reputation'
log_scale = False
x_lims = [0,0.5]
y_lims = [0, 1.1]

################################################################################

import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import csv
import os
import re
import sys
import random as rnd

x_list = []
fc_list = []
fit_list = []
model_list = []

# x values for the fit
fit_x = np.linspace(0, 1, 100)

for d in dirs:
    os.chdir(d)
    all_files = os.listdir() # get list of all files in the working directory
    files = []
    #print(all_files)
    for f in all_files:
        text_file = re.search('csv', f)
        if text_file is not None:
                files.append(text_file.string)
    #files.remove('outputs')
        
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


    #####################
    #      Fitting
    ####################

    ### for polynomial fit of degree d, use pfit and fit. Uncomment this region
    #pfit = np.polyfit(x, fc, 2)
    #fit = np.poly1d(pfit)
    #fit_list.append(fit)
    
    ### for a linear fit with fixed intercept, use model. Uncomment this region
    #model = sm.OLS(fc - 0.5, x).fit()        
    #model_list.append(model)
    
    ### plotting the actual data points as background to the fit
    #plt.plot(x, fc, 'k-', linewidth=0.5, alpha=0.7)
    
    ### If not fit is required
    
    legend_label = legend[dirs.index(d)]      
    plt.plot(x, fc, linewidth=1, label=legend_label)
    
    x_list.append(x)
    fc_list.append(fc)
    os.chdir('..') # go back to the parent directory

### plotting all the fits 

# for fit in fit_list:

    ### legends
    #legend_label = legend[model_list.index(model)]
    #legend_label = legend[fit_list.index(fit)]
    #slope = pfit[0]
    #intercept = pfit[1]
    #line = str(round(slope, 3))+'$x + $' + str(round(intercept, 2))
    
    ### plots
    #plt.plot(fit_x,(0.5+model.predict(fit_x)), label=legend_label)
    #plt.plot(fit_x,fit(fit_x), label=legend_label, linewidth=1)
    # + ' (' + line+')'
    
    #plt.ylabel('Fraction of cooperators')
    #plt.xlabel('r')
    #plt.xlim([0,0.5])
    #plt.ylim([0,1])
    

plt.title(plot_title)
plt.ylabel('Fraction of Cooperators ($f_{C}$)')
plt.xlabel('$r$')

if  log_scale:
    plt.xscale('log')

plt.xlim(x_lims)
plt.ylim(y_lims)

plt.legend()
plt.show()

    
