import os
import numpy as np
import pandas as pd

# pd.set_option("display.max_rows", None, "display.max_columns", None)

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

    print('vVvV')

    t_min = df.index.min()
    t_max = df.index.max()

    data_freq = (df.index[1] - t_min).total_seconds() / 60.0
    if data_freq != freq: 
        print('DATA FREQUENCY OF FIRST TWO DATA POINTS '+\
            'AND USER-INPUT FREQUENCY DO NOT MATCH')

    # use data file number in path as a check on df length
    data_len_check = len(os.listdir(path))

    # after check_duplicate_ind_remove is called
    if updated_len is not None: 
        data_len_check = updated_len

    diff_minute = (t_max - t_min).total_seconds() / 60.0

    print('read in '+var+' from '+str(t_min)+' to '+str(t_max)+\
        ' every '+str(freq)+' minutes, total of '+str(data_len_check)+' files')

    if data_len_check != (diff_minute + freq) / freq: 

        print('!!!!!!!!!!')
        print('!!!!!!!!!!')
        print('WARNING: '+var+' DATA FILE NUMBER ('+str(data_len_check)+\
            ') DOES NOT MATCH DEFINED DATA FREQUENCY ('+str(freq)+')')
        print('!!!!!!!!!!')
        print('!!!!!!!!!!')

    # if data_len_check != (diff_minute + freq) / freq: 

        print('wrong')
        
        # have duplicated rows in df
        if data_len_check > (diff_minute + freq) / freq: 

            df = check_duplicate_ind_remove(df)

            print('after checking dup')
            print(len(df))
                
            print('verify data again...')
            # recursion, to verify the data again
            df = verify_data_file_count(df, var, path, freq, updated_len=len(df))

            return df

        # have missing rows in df
        elif data_len_check < (diff_minute + freq) / freq: 

            df = check_missing_ind_add_nan(df, t_min, t_max, freq)

            print('after checking miss')
            print(len(df))
                
            print('verify data again...')
            # recursion, to verify the data again
            # verify_data_file_count(df, var, path, freq, updated_len=len(df))

            
            df = verify_data_file_count(df, var, path, freq, updated_len=len(df))

            return df

    else: 

        print('right')
        print(len(df))

    # print('lennn')
    # print(len(df))
    # print('whole fn')

        return df
        
    
        # print('sodar df len')
        # print(len(df))
        # print('1 time')

        # return df

    # print('lennn')
    # print(len(df))
    # return df