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
    all_lines = f.readlines()
    tally_line = all_lines[-15]
    data = tally_line.split()
    outp_info['tally total'] = float(data[1])
    outp_info['error total'] = float(data[2])
    outp_info['vov'] = float(data[3])
    outp_info['slope'] = float(data[4])
    outp_info['fom'] = float(data[5])
    outp_info['cpu time'] = float(all_lines[-3].split(' ')[-2])
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


def iterate_refine(fdir, refine):
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
        if factor[-3:] == '.sh':
            continue
        new_dir = fdir + '/' + factor
        collected_info = collect_info(new_dir)

        # concactenate dictionaries and append to total list
        info = {refine: float(factor)}
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

            deci_info = iterate_refine(fdir + '/decimate', 'decimation')
            wwig_df = pd.DataFrame(deci_info)
            wwig_df.to_csv('csv/wwig_deci_data.csv', index_label='i')

            rough_info = iterate_refine(fdir + '/rough', 'perturbation')
            wwig_df = pd.DataFrame(rough_info)
            wwig_df.to_csv('csv/wwig_rough_data.csv', index_label='i')

        elif mode in ['cwwm', 'analog', 'reference']:
            all_info = collect_info(fdir)
            mode_dir = {'mode': mode}
            all_info.update(mode_dir)
            # make pandas df and write to file
            info_df = pd.DataFrame([all_info])
            save_name = 'csv/' + mode + '_data.csv'
            info_df.to_csv(save_name, index_label='i')
