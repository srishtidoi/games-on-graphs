#! /bin/sh

#### parameters

population=1600
eps=20
network=scalefree
rule=bayesian

#### make and cd to new directory
#### add comments at the end (more_r, more_t, etc.)

dirname="phase_diagrams_n"$population"e"$eps"_"$network"_"$rule'_'
mkdir $dirname
cd $dirname

#### run the simulation
python3 ../main.py $population $eps $network $rule | tee zoutput.txt

### split output file
#mkdir outputs
#mv zoutput.txt outputs
#cd outputs
#split -l 1000000 -d --additional-suffix=.txt zoutput.txt file
