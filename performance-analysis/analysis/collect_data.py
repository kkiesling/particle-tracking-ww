import sys
import os
from numpy.lib.npyio import save
import pandas as pd


def read_wwchecks(fpath):
    """read ww files info and collect information

    Inputs:
    -------
        fpath: string, path to ww_checks file

    Returns:
    --------
        ww_info: dictionary of info from the ww_checks file
    """
    ww_info = {}
    f = open(fpath, "r")
    all_lines = f.readlines()
    for line in all_lines[1:]:
        [metric, value] = line.split(':')
        metric = metric[1:]  # get rid of leading space on all
        ww_info[metric] = float(value.strip())  # convert to number
    f.close()
    return ww_info


def read_outp(fpath):
    """read tally info and performance info from outp file

    Input:
    ------
        fpath: string, path to outp file

    Returns:
    --------
        outp_info: dictionary containing tally 24 results for each
            energy group and FOM data
    """
    outp_info = {}
    f = open(fpath, "r")
    line = f.readline()
    end = False
    while not end:
        if '1tally       24' in line:
            # found tally result data
            for i in range(9):
                # skip some lines
                f.readline()
            for i in range(4):
                # read tally data
                data = f.readline().split()
                if data[0] == 'total':
                    energy = data[0]
                else:
                    energy = float(data[0])
                result = float(data[1])
                error = float(data[2])
                outp_info[energy] = (result, error)

        if 'nps      mean     error   vov  slope    fom' in line:
            # found FOM data
            for i in range(13):
                # skip to last line of list
                line = f.readline()
            # collect data from tall 24 only
            data = line.split()
            outp_info['vov'] = data[8]
            outp_info['slope'] = data[9]
            outp_info['fom'] = data[10]

            # all info has been collected
            end = True
        line = f.readline()

    return outp_info


def iterate_ratios(fdir, factor_name=None, factor_val=None):
    """Iterate through each ratio directory collecting necessary info

    Inputs:
    -------
        fdir: str, ath to folder with ratio folders
        factor_name: str, dc or sm for decimating or smoothing
        factor_val: float, value of the dc or sm that was applied

    Returns:
    --------
        all_info: dict, collected metrics info from outp and ww_checks
            files along with run information if applicable for all
            ratio folders provided
    """
    all_info = []
    for ratio in os.listdir(fdir):
        new_dir = fdir + '/' + ratio
        ww_info = {}
        outp_info = {}
        for f in os.listdir(new_dir):
            # find outp and ww_checks files
            fpath = new_dir + '/' + f
            if f == 'ww_checks':
                ww_info = read_wwchecks(fpath)
            elif f == 'outp':
                outp_info = read_outp(fpath)

        # concactenate dictionaries and append to total list
        ratio_info = {'ratio': int(ratio[1:])}
        ratio_info.update(ww_info)
        ratio_info.update(outp_info)

        if factor_name:
            # if smoothing or decimating factor, need to add value to dict
            factor_dict = {factor_name: factor_val}
            ratio_info.update(factor_dict)

        all_info.append(ratio_info)

    return all_info


if __name__ == '__main__':

    fpath = sys.argv[1]  # path to results folder

    for mode in os.listdir(fpath):
        fdir = fpath + '/' + mode

        if mode == 'wwig':
            for category in os.listdir(fdir):
                new_dir = fdir + '/' + category

                if category == 'default':
                    all_info = iterate_ratios(new_dir)
                    default_df = pd.DataFrame(all_info)
                    default_df.to_csv('wwig_default_data.csv', index_label='i')

                elif category in ['dc', 'sm']:
                    collected_info = []
                    for factor in os.listdir(new_dir):
                        factor_dir = new_dir + '/' + factor
                        # get ratio info from each factor
                        fval = float(factor.split('0')[-1])
                        all_info = iterate_ratios(factor_dir, factor_name=category,
                                                  factor_val=fval)
                        collected_info.extend(all_info)

                    factor_df = pd.DataFrame(collected_info)
                    save_name = 'wwig_' + category + '_data.csv'
                    factor_df.to_csv(save_name, index_label='i')

        elif mode in ['cwwm', 'analog']:
            # read outp info for both modes
            outp_path = fdir + '/' + 'outp'
            metrics_info = read_outp(outp_path)
            if mode == 'cwwm':
                ww_path = fdir + '/' + 'ww_checks'
                # get ww check info for cwwm mode
                ww_info = read_wwchecks(ww_path)
                metrics_info.update(ww_info)

            # make pandas df and write to file
            info_df = pd.DataFrame(metrics_info)
            save_name = mode + '_data.csv'
            info_df.to_csv(save_name)
