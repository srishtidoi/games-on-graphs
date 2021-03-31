#! /bin/sh

#### parameters

population=100
eps=20
network=smallworld
rule=bayesian

#### make and cd to new directory
#### add comments at the end (more_r, more_t, etc.)

dirname=$network"_"$rule"_n"$population"e"$eps"_test"
mkdir $dirname
cd $dirname
mkdir outputs

#### run the simulation
python3 ../main.py $population $eps $network $rule | tee outputs/zoutput.txt

### split output file
cd outputs
split -l 1000000 -d --additional-suffix=.txt zoutput.txt file

### plot the graph
cd ..
python3 ../plotting/plot_indir.py $eps save


