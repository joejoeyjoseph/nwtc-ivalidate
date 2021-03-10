import os
import numpy as np

def convert_mask_to_nan(var, t): 

    if np.ma.is_masked(var) is True: 

        var = np.NaN

        print('detect masked value at '+str(t)+', convert to NaN')

    return var

def convert_flag_to_nan(var, flag, t): 

    if var == flag: 

        var = np.NaN

        print('detect flagged value at '+str(t)+', convert to NaN')

    return var

def test():

    print('checkkk')

def verify_data_file_count(df, var, path, freq): 

    t_min = df.index.min()
    t_max = df.index.max()
    data_file_num = len(os.listdir(path))

    diff_minute = (t_max - t_min).total_seconds() / 60.0

    print('read in '+var+' from '+str(t_min)+' to '+str(t_max)+\
        ' every '+str(freq)+' minutes, total of '+str(data_file_num)+' files')

    if data_file_num == (diff_minute + freq) / freq: 
        pass
    else: 
        print(var+' DATA FILE NUMBER ('+str(data_file_num)+\
            ') DOES NOT MATCH DEFINED DATA FREQUENCY ('+str(freq)+')')

    return 