import os
import numpy as np
import pandas as pd

# pd.set_option("display.max_rows", None, "display.max_columns", None)

def convert_mask_to_nan(var, t, mask_i): 

    if np.ma.is_masked(var) is True: 

        var = np.NaN

        if mask_i == 0: 

            print()

        mask_i += 1

        print('detect masked value at '+str(t)+', convert to NaN')

    return var, mask_i

def convert_flag_to_nan(var, flag, t): 

    if var == flag: 

        var = np.NaN

        print('detect flagged value at '+str(t)+', convert to NaN')

    return var

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

def check_missing_ind_add_nan(df, t_min, t_max, freq): 

    ideal = pd.date_range(start=t_min, end=t_max, freq=str(freq)+'min')
    with_data = ideal.isin(df.index)

    print('DETECT '+str(len(ideal[~with_data]))+' ROWS IN DATAFRAME ARE MISSING')
    print('THEY ARE:')
    print(ideal[~with_data].strftime("%Y-%m-%d %H:%M:%S").values)

    ideal_df = pd.DataFrame(data=np.NaN, columns=df.columns+'_i', index=ideal)
    ideal_df.index.name = df.index.name

    new_df = pd.concat([ideal_df, df], axis=1)

    df = new_df[df.columns]

    return df

def verify_data_file_count(df, var, path, freq, updated_len=None): 

    t_min = df.index.min()
    t_max = df.index.max()

    data_freq = (df.index[1] - t_min).total_seconds() / 60.0
    if data_freq != freq: 
        print()
        print('!!!!!!!!!!')
        print('WARNING: DATA FREQUENCY OF FIRST TWO DATA POINTS '+\
            'AND USER-INPUT FREQUENCY DO NOT MATCH')
        print('!!!!!!!!!!')

    # use data file number in path as a check on df length
    data_len_check = len(os.listdir(path))

    # after check_duplicate_ind_remove is called
    if updated_len is not None: 
        data_len_check = updated_len

    diff_minute = (t_max - t_min).total_seconds() / 60.0

    print()
    print('read in '+var+' from '+str(t_min)+' to '+str(t_max))
    print('every '+str(freq)+' minutes, total of '+str(data_len_check)+' files')

    desired_len = (diff_minute + freq) / freq

    if data_len_check != desired_len: 

        print()
        print('!!!!!!!!!!')
        print('WARNING: '+var+' DATA FILE NUMBER ('+str(data_len_check)+\
            ') DOES NOT MATCH DESIRED DATA LENGTH ('+str(desired_len)+\
            '), WHICH IS DEFINED BY DATA START TIME ('+str(t_min)+\
            '), DATA END TIME ('+str(t_max)+\
            '), AND USER-INPUT DATA FREQUENCY ('+str(freq)+')')
        print('!!!!!!!!!!')

    # if data_len_check != (diff_minute + freq) / freq: 
        
        # have duplicated rows in df
        if data_len_check > desired_len: 

            df = check_duplicate_ind_remove(df)

            print()
            print('verify data again...')
            # recursion, to verify the data again
            df = verify_data_file_count(df, var, path, freq, updated_len=len(df))

            return df

        # have missing rows in df
        elif data_len_check < desired_len: 

            df = check_missing_ind_add_nan(df, t_min, t_max, freq)
            
            print()
            print('verify data again...')
            # recursion, to verify the data again           
            df = verify_data_file_count(df, var, path, freq, updated_len=len(df))

            return df

    else: 

        print()
        print('--- '+var+' dataframe should have unique and continuous data ---')

        return df