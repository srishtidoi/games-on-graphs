#! /bin/sh

### use this to display a plot of n<neps number of eps, or when sim is going on
### requires you to be in the directory with all the sim data
### argument is number of eps to plot

path="/home/srish/padhai/projectplis/santh/code/plotting"
python3 $path/plot_indir.py $1 show
