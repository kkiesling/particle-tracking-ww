import sys
import os
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
        if '1tally        2' in line:
            # found tally result data
            for i in range(9):
                f.readline()
            for i in range(29):
                # read tally data - get total only
                data = f.readline().split()
                if data[0] == 'total':
                    energy = data[0]
                    result = float(data[1])
                    error = float(data[2])
                    res_key = 'tally ' + energy
                    err_key = 'error ' + energy
                    outp_info[res_key] = result
                    outp_info[err_key] = error

        if 'nps      mean     error   vov  slope    fom' in line:
            # found FOM data
            for i in range(20):
                # skip to last line of list
                line = f.readline()
                data = line.split()
                if data[0] in ['50000', '1000000']:
                    # collect data from tally 2
                    outp_info['vov'] = data[3]
                    outp_info['slope'] = data[4]
                    outp_info['fom'] = data[5]
                    break

            # all info has been collected
            end = True
        line = f.readline()

    return outp_info


def collect_info(fdir):

    # files
    ww_path = fdir + '/ww_checks'
    outp_path = fdir + '/outp'
    meshtal_path = fdir + '/meshtal'

    # get info
    if os.path.exists(ww_path):
        ww_info = read_wwchecks(ww_path)
    else:
        ww_info = {}
    outp_info = read_outp(outp_path)

    # consolidate
    outp_info.update(ww_info)
    return outp_info


def iterate_ratios(fdir):
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
        collected_info = collect_info(new_dir)

        # concactenate dictionaries and append to total list
        info = {'ratio': int(ratio[1:])}
        info.update(collected_info)
        mode_dir = {'mode': 'wwig'}
        info.update(mode_dir)

        all_info.append(info)

    return all_info


def iterate_decimation(fdir):
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
    for factor in os.listdir(fdir):
        new_dir = fdir + '/' + factor
        collected_info = collect_info(new_dir)

        # concactenate dictionaries and append to total list
        info = {'ratio': float(factor)}
        info.update(collected_info)
        mode_dir = {'mode': 'wwig'}
        info.update(mode_dir)

        all_info.append(info)

    return all_info


if __name__ == '__main__':

    fpath = sys.argv[1]  # path to results folder

    for mode in os.listdir(fpath):
        fdir = fpath + '/' + mode

        if mode == 'wwigs':
            ratio_info = iterate_ratios(fdir + '/ratios')
            wwig_df = pd.DataFrame(ratio_info)
            wwig_df.to_csv('csv/wwig_ratio_data.csv', index_label='i')

            deci_info = iterate_decimation(fdir + '/decimate')
            wwig_df = pd.DataFrame(deci_info)
            wwig_df.to_csv('csv/wwig_deci_data.csv', index_label='i')

        elif mode in ['cwwm', 'analog', 'reference']:
            all_info = collect_info(fdir)
            mode_dir = {'mode': mode}
            all_info.update(mode_dir)
            # make pandas df and write to file
            info_df = pd.DataFrame([all_info])
            save_name = 'csv/' + mode + '_data.csv'
            info_df.to_csv(save_name, index_label='i')
