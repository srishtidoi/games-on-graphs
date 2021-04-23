#! /bin/sh

#### parameters

note=rep
population=100
eps=100
network=scalefree
rule=reputation

#### make and cd to new directory

dirname=$network"_"$rule"_n"$population"e"$eps"_"$note
mkdir $dirname
cd $dirname
mkdir outputs

#### run the simulation
python3 ../main.py $population $eps $network $rule 

#| tee outputs/zoutput.txt

### split output file
#cd outputs
#split -l 1000000 -d --additional-suffix=.txt zoutput.txt file

### plot the graph
#cd ..
python3 ../plotting/plot_indir.py $eps save


