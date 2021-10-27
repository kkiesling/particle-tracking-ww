#!/usr/bin/bash

export HOME=/home/cnerg/
source /home/cnerg/.bashrc

# set datapath
export DATAPATH=/staging/kkiesling/MCNP_DATA

# run mcnp
mcnp6 i=cwwm.inp wwinp=wwinp_magic

