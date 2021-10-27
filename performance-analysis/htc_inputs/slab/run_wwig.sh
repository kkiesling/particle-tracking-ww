#!/usr/bin/bash

export HOME=/home/cnerg/
source /home/cnerg/.bashrc

# set datapath
export DATAPATH=/staging/kkiesling/MCNP_DATA



# only use the "no viz" ones
rm -r 000/vols/ 000/levelfile 000/visitlog.py
mv 000/wwn_000_noviz.h5m 000/wwn_000.h5m

echo `ls -l .`
echo `ls -l 000/`
echo `pwd`

mcnp6 i=wwig_slab.inp wcad=000/

