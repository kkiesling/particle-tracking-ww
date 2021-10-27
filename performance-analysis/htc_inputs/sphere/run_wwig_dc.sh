#!/usr/bin/bash

export HOME=/home/cnerg/
source /home/cnerg/.bashrc

# set datapath
export DATAPATH=/staging/kkiesling/MCNP_DATA

# run mcnp

export r=$1
export s=$2

# only use the "no viz" ones (need to rename?)
for g in 0 1 2
do
mv r${r}/wwn_00${g}_d${s}_noviz.h5m r${r}/wwn_00${g}.h5m
rm r${r}/wwn_00${g}_d${s}.h5m
done

mcnp6 i=wwig.inp wcad=r${r}/

