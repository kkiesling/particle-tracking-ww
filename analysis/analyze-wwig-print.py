import pandas as pd
import sys
import math as m


def parse_line(line):
    """deterimine what information is on the line"""

    linesplit = line.split(":")
    keyname = linesplit[0]
    info = linesplit[1]

    if "Position" in keyname:
        key = 'xyz'
        str_lst = info.strip().split()
        x = float(str_lst[0])
        y = float(str_lst[1])
        z = float(str_lst[2])
        val = (x, y, z)
    else:
        val = float(info.strip())
        if "Energy (mcnp)" in keyname:
            key = 'Energy'
        elif "E_low" in keyname:
            key = "E_low"
        elif "E_upper" in keyname:
            key = "E_hi"
        elif "Pre-WW" in keyname:
            key = 'w_i'
        elif "WW Low bound" in keyname:
            key = 'ww_l'
        elif "WW Up bound" in keyname:
            key = 'ww_u'
        elif "Post-WW" in keyname:
            key = 'w_p'

    return key, val


def read_file(fname, wdf):
    """read file line by line and populate dataframe"""

    i = -1  # initial index
    with open(fname, 'r') as f:
        for line in f:
            if "****" in line:
                # new event, so index i and go to next line
                i += 1
            else:
                # populate current event with information
                key, val = parse_line(line)
                wdf.loc[i, key] = val


def check_position(wdf):
    """for a given position and energy, check that it is on a wwig surface"""

    # WWIG geometry info:

    # geom extents for y and z:
    y_surfs = [-5., 5.]
    z_surfs = [-5., 5.]

    # x surface locations based on energy
    # key = energy bounds (E_low, E_high)
    # value = list of locations
    ex_surfs = {(1.e-11, 1.5e-2): [0, 1, 6, 11, 16, 20],
                (1.5e-2, 1.5e-1): [0, 2, 7, 12, 17, 20],
                (1.5e-1, 4.0e-1): [0, 3, 8, 13, 18, 20],
                (4.0e-1, 9.0e-1): [0, 4, 9, 14, 19, 20],
                (9.0e-1, 1.5e0): [0, 5, 10, 15, 20]}

    for i, row in wdf.iterrows():
        # get position and energy information
        x = row['xyz'][0]
        y = row['xyz'][1]
        z = row['xyz'][2]
        energy = row['Energy']
        e_bounds = (row['E_low'], row['E_hi'])
        x_surfs = ex_surfs[e_bounds]

        if (x in x_surfs) or (y in y_surfs) or (z in z_surfs):
            row['location check'] = True
        else:
            row['location check'] = False


def check_weight(wdf):
    """for a given W_l and W_u on the wwig surface, check that the
    weight is properly updated"""

    for i, row in wdf.iterrows():
        w_i = row['w_i']
        w_p = row['w_p']
        ww_l = row['ww_l']
        ww_u = row['ww_u']
        ww_s = 3.*ww_l

        # check w_p for each of the three options
        if w_i < ww_l:
            # particle weight is below w_l so terminate (nan) or survive with
            # survival weight ww_s
            if (w_p == ww_s) or (m.isnan(w_p)):
                row['weight check'] = True
            else:
                row['weight check'] = False
        elif ww_l < w_i < ww_u:
            # particle weight is w/in window so no change
            if w_p == w_i:
                row['weight check'] = True
            else:
                row['weight check'] = False
        elif w_i > ww_u:
            # particle splits according to ww_u
            if ww_u == 0:
                # edge of boundary
                n_split = 1
            else:
                n_split = m.ceil(w_i/ww_u)
                if (n_split > 5):
                    # max splits specified by mcnp
                    n_split = 5
            if (w_p == w_i/n_split):
                row['weight check'] = True
            else:
                row['weight check'] = False


def analyze_data(wdf):

    total = wdf.shape[0]

    print("Total wwval checks recorded: {}".format(total))

    # check locations of look-ups:
    check_position((wdf))
    n_pos_correct = len(wdf[wdf['location check'] == True])
    pos_percent = float(n_pos_correct) / float(total) * 100.
    print("{} % of wwval checks occur on a surface".format(pos_percent))

    # check that weights are properly being applied
    check_weight(wdf)
    n_w_correct = len(wdf[wdf['weight check'] == True])
    w_percent = float(n_w_correct) / float(total) * 100.
    print("{} % of weight checks are correct".format(w_percent))


if __name__ == "__main__":

    # output file to analyze
    fname = sys.argv[1]

    # initialize pandas data structure
    # position (x, y, z), particle energy, ww lower and upper energy bounds,
    #   wwig surface W_l and W_u bounds, initial weight, post wwval weight
    columns = ['xyz', 'Energy', 'E_low', 'E_hi',
               'ww_l', 'ww_u', 'w_i', 'w_p',
               'location check', 'weight check']
    wdf = pd.DataFrame(columns=columns)

    # read file and populate dataframe
    read_file(fname, wdf)

    # analyze data
    analyze_data(wdf)
