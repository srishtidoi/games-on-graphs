#! /bin/sh

#### parameters ----->
#### note: note for this particular sim (test, newmodel, p0.7, etc)
#### eps: number of runs
#### network: scalefree, smallworld, lattice, RR (random regular)
#### rule: learning rule - imitate, bayesian, reputation
#### out: kind of output - null, rep (for time evolution of reputation parameter) 

note=test
population=100
eps=2
network=scalefree
rule=reputation
out=null

#### make and cd to new directory

dirname=$network"_"$rule"_n"$population"e"$eps"_"$note
mkdir $dirname
cd $dirname
mkdir outputs

#### run the simulation
python3 ../main.py $population $eps $network $rule $out

#### add this to direct the print output to a text file and then split it
#| tee outputs/zoutput.txt
#cd outputs
#split -l 1000000 -d --additional-suffix=.txt zoutput.txt file

### plot the graph
#cd ..
python3 ../plotting/plot_indir.py $eps save


