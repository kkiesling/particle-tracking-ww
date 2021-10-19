import dagmc_stats.DagmcFile as df
import dagmc_stats.DagmcQuery as dq
import sys
import numpy as np
import os

if __name__ == "__main__":

    flist = sys.argv[1:]

    for f in flist:
        fsize = os.path.getsize(f) / (1024.**2)

        gfile = df.DagmcFile(f)
        gqu = dq.DagmcQuery(gfile)
        gqu.calc_coarseness()

        print(f)
        print('file size (MB): {}'.format(fsize))
        print(gqu._surf_data)
        print('average: {}'.format(np.average(gqu._surf_data['coarseness'])))
