import numpy as np
import matplotlib
import ternary
import csv
import os
import sys

matplotlib.rcParams['figure.dpi'] = 200
#matplotlib.rcParams['figure.figsize'] = (4, 4)

dirname = sys.argv[1] # give the name of the directory as an argument
os.chdir(dirname) # change working directory 
all_files = os.listdir() # get list of all files in the working directory

n_eps = int(sys.argv[2]) # give the number of eps you want to plot
if n_eps == 'a':
    files = all_files
else:
    files = all_files[:n_eps]
    
episodes_sum = np.array([])
for filename in files:
    points = []
    cols = []

    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        cols = next(csvreader) # column headings out of the way
        
        for row in csvreader:
            points.append([float(row[1]), 1 - float(row[1]) - float(row[2]), float(row[2])])
    print(points[2])
    points_array = np.array(points)
    print(points_array[2])
    if episodes_sum.size > 0:
        if episodes_sum.size > points_array.size:
            points_array.resize(episodes_sum.shape)
            episodes_sum += points_array
        else:
            episodes_sum.resize(points_array.shape)
            episodes_sum += points_array
    else:
        episodes_sum = np.array(points)

    print(episodes_sum[2])
    
points_avg = episodes_sum/len(files)
print(points_avg[2])
# Plotting trajectory 
figure, tax = ternary.figure(scale=1.0)
figure.set_size_inches(5, 5)

fontsize = 10
tax.boundary()
tax.gridlines(multiple=0.2, color="black")
#tax.set_title("Dynamics\n", fontsize=10)
tax.right_corner_label("C", fontsize=fontsize)
tax.top_corner_label("D", fontsize=fontsize)
tax.left_corner_label("L", fontsize=fontsize)

# Plot the data
tax.plot(points_avg, linewidth=1.0, label="Curve")
#tax.ticks(axis='lbr', multiple=0.1, linewidth=1, tick_formats="%.1f", offset=0.02)

tax.get_axes().axis('off')
tax.clear_matplotlib_ticks()
tax.show()

