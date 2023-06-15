#!/usr/bin/env sh
touch PileUps.tar ; rm PileUps.tar

python ../python/PUcollector.py ../data/2016ReReco_Moriond17.json
python ../python/PUcollector.py ../data/2017ReReco_WinterMC.json
python ../python/PUcollector.py ../data/2018ReReco_JuneProjectionFull18.json
python ../python/PUcollector.py ../data/UL2016_PoissonOOTPU.json
python ../python/PUcollector.py ../data/UL2017_PoissonOOTPU.json
python ../python/PUcollector.py ../data/UL2018_PoissonOOTPU.json
tar -cf PileUps.tar 201* UL201*
