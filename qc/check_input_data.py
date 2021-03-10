import os
import numpy as np
import pandas as pd

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

def check_duplicate_ind_remove(df): 

    if df.index.has_duplicates: 

        pd.set_option("display.max_rows", None, "display.max_columns", None)

        dup_ind = df.index.duplicated(keep='first')

        print('DETECT '+str(dup_ind.sum())+' ROWS IN DATAFRAME ARE DUPLICATED')
        print('THEY ARE:')
        print(df.iloc[dup_ind])

        print('REMOVE DUPLICATED ROWS')
        df = df[~dup_ind]

    return df

def verify_data_file_count(df, var, path, freq, updated_len=None): 

    t_min = df.index.min()
    t_max = df.index.max()

    # use data file number in path as a check on df length
    data_len_check = len(os.listdir(path))

    # after check_duplicate_ind_remove is called
    if updated_len is not None: 
        data_len_check = updated_len

    diff_minute = (t_max - t_min).total_seconds() / 60.0

    print('read in '+var+' from '+str(t_min)+' to '+str(t_max)+\
        ' every '+str(freq)+' minutes, total of '+str(data_len_check)+' files')

    if data_len_check == (diff_minute + freq) / freq: 

        pass

    else: 

        print('!!!!!!!!!!')
        print('!!!!!!!!!!')
        print('WARNING: '+var+' DATA FILE NUMBER ('+str(data_len_check)+\
            ') DOES NOT MATCH DEFINED DATA FREQUENCY ('+str(freq)+')')
        print('!!!!!!!!!!')
        print('!!!!!!!!!!')

        df = check_duplicate_ind_remove(df)

        print('verify data again...')
        # recursion, to verify the data again
        verify_data_file_count(df, var, path, freq, updated_len=len(df))

    return df