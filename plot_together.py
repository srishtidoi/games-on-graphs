import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import csv
import os
import re
import sys
import random as rnd

# list of directories with the phase diagrams
dirs = ['scalefree_reputation_n100e100_p0.3', 'scalefree_reputation_n100e100_fr_p0.3']
    #'pi0.0','pi0.5','pi0.5_onlyrep','pi0.5_onlyrep_tend0.5','pi0.5_tend0.5','pi0.7','pi0.9','pi1.0','pi1.0_tend0.5']

    # list of p values
legend = ['without $f_{R}$', 'with $f_{R}$']
    #'$p=0.0$','$p=0.5$','$p=0.5$ (info only for rep)','$p=0.5$ (info only for rep, constant tendency = 0.5)','$p=0.5$ (contant tendency = 0.5)', '$p=0.7$', '$p=0.9$','$p=1.0$','$p=1.0$ (constant value of tendency = 0.5)']
    #'$p=0.7, p_{info}=0.0$','$p=0.7, p_{info}=0.3$','$p=0.7, p_{info}=0.5$','$p=0.7, p_{info}=0.7$']

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


    ### fitting
    #pfit = np.polyfit(x, fc, 2)
    #fit = np.poly1d(pfit)      # polynomial fit
    #model = sm.OLS(fc - 0.5, x).fit()         # linear fit with fixed intercept
    #plt.plot(x, fc, 'k-', linewidth=0.5, alpha=0.7)
    
    ### if no fit is needed
    
    legend_label = legend[dirs.index(d)]      
    plt.plot(x, fc, linewidth=1, label=legend_label)
    
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
    

plt.title('Network: Scalefree, Model: Reputation')
plt.ylabel('Fraction of Cooperators ($f_{C}$)')
plt.xlabel('$r$')
#plt.xscale('log')
plt.xlim([0,0.5])
plt.ylim([0,1.1])

plt.legend()
plt.show()

    
