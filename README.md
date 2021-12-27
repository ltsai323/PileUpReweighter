# Introduction
A pile-up reweighting calculator.
A json file is needed to define the inputs.
The output is root files that contains a histogram 'mcwei_run000001'.

# Usage
``python python/PUcollector.py your.json``  
Prepare your json file contains two fragments :
- "gitsource" means the files from github. The cms-sw file from SimGeneral/Mixingmodule/python
- "dataTarget" is the local path to data pileup.
# Note
- The probability density function at MC mixing contains some 0 value. Once the values are found, the weighting value is forced to 0 even if non-zero probability found in data at that bin.
- 0 means 1e-10 in float.

# Installation
``sh -c "$(wget https://raw.githubusercontent.com/ltsai323/PileUpReweighter/main/install.sh -O-)" ``
