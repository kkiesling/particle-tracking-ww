#!/bin/bash

for d in `seq 1 8`
do
cd 0.${d}/
rm out* meshta* runtp* ww_checks
mcnp6 i= ../../../../../inputs/wwig_slab.inp wcad= ../../../../../wwigs_slab/decimated/0.${d}
cd ..
done

cd ../ratios/r8/
rm out* meshta* runtp* ww_checks
mcnp6 i= ../../../../../inputs/wwig_slab.inp wcad= ../../../../../wwigs_slab/r8/geoms
