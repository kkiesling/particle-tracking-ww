#!/usr/bin/bash

export HOME=/home/cnerg/
source /home/cnerg/.bashrc

# set datapath
export DATAPATH=/staging/kkiesling/MCNP_DATA

# only use the "no viz" ones
mkdir geoms
mv wwn_000_noviz.h5m geoms/wwn_000.h5m

mcnp6 i=wwig_slab.inp wcad=geoms/
