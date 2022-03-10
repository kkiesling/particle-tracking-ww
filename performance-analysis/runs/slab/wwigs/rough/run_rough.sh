#!/bin/bash

for d in `seq 1 8`
do
cd 0.${d}/
rm  out* meshta* runtp* ww_checks
mcnp6 i= ../../../../../inputs/wwig_slab.inp wcad= ../../../../../wwigs_slab/rougher/0.${d}/
cd ..
done

for d in `seq 0 5`
do
cd 1.${d}/
rm  out* meshta* runtp* ww_checks
mcnp6 i= ../../../../../inputs/wwig_slab.inp wcad= ../../../../../wwigs_slab/rougher/1.${d}/
cd ..
done

