#!/bin/bash
#SBATCH --job-name=cadis-krk
#SBATCH --partition=pre
#SBATCH --time=1:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=20
#SBATCH --mem-per-cpu=6400
#SBATCH --error=screen_err
#SBATCH --output=screen_out
set -e
source /software/groups/dagmc/etc/load_advantg_3.0.3.sh
advantg cadis.inp
