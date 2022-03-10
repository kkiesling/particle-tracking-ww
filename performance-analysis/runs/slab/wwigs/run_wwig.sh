#!/bin/bash

# run rough first
#cd rough/
#for d in `seq 1 8`
#do
#cd 0.${d}/
#rm  out* meshta* runtp* ww_checks
#mcnp6 i= ../../../../../inputs/wwig_slab.inp wcad= ../../../../../wwigs_slab/rougher/0.${d}/
#cd ..
#done

#for d in `seq 0 5`
#do
#cd 1.${d}/
#rm  out* meshta* runtp* ww_checks
#mcnp6 i= ../../../../../inputs/wwig_slab.inp wcad= ../../../../../wwigs_slab/rougher/1.${d}/
#cd ..
#done

# run decimated
cd decimate/
for d in 6 7
do
cd 0.${d}-redo/
rm out* meshta* runtp* ww_checks
mcnp6 i= ../../../../../inputs/wwig_slab.inp wcad= ../../../../../wwigs_slab/decimated/0.${d}
cd ..
done

# run ratio
cd ../ratios/
for d in 15
do
cd r${d}-redo/
rm out* meshta* runtp* ww_checks
mcnp6 i= ../../../../../inputs/wwig_slab.inp wcad= ../../../../../wwigs_slab/ratio/r${d}/geoms/
cd ..
done
