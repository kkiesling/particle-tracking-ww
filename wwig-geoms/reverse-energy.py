from pymoab import core
import sys
import os
import glob


def set_conversion():

    evals = [1e-08, 3e-08, 5e-08, 1e-07, 2.25e-07, 3.25e-07, 4.1399e-07,
           8e-07, 1e-06, 1.1253e-06, 1.3e-06, 1.8554e-06, 3.059e-06,
           1.0677e-05, 2.9023e-05, 0.0001013, 0.00058295, 0.0030354,
           0.015034, 0.11109, 0.40762, 0.90718, 1.4227, 1.8268,
           3.0119, 6.3763, 20.0]

    conversion = {}
    for i, erg in enumerate(evals):
        if i == 0:
            conversion[i] = [erg, 0.0]
        else:
            conversion[i] = [erg, evals[i-1]]

    return conversion




if __name__ == '__main__':

    conversion = set_conversion()

    for fname in glob.glob(os.getcwd() + '/*.h5m'):

        IDstr = fname.split('/')[-1].split('.')[0].split('_')[1]
        ID = int(IDstr)
        print('Converting ' + IDstr)

        mb = core.Core()
        mb.load_file(fname)
        rs = mb.get_root_set()

        eup_eh = mb.tag_get_handle('E_UP_BOUND')
        elo_eh = mb.tag_get_handle('E_LOW_BOUND')

        print('before:')
        print('up bound ' + str(mb.tag_get_data(eup_eh, rs)))
        print('lo bound ' + str(mb.tag_get_data(elo_eh, rs)))

        mb.tag_set_data(eup_eh, rs, conversion[ID][0])
        mb.tag_set_data(elo_eh, rs, conversion[ID][1])

        print('after')
        print('up bound ' + str(mb.tag_get_data(eup_eh, rs)))
        print('lo bound ' + str(mb.tag_get_data(elo_eh, rs)))

        new_name = 'rwwn_{}.h5m'.format(IDstr)
        mb.write_file(new_name)
