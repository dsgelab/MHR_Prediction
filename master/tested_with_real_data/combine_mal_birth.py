# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 12:42:55 2020

@author: Atte
"""
import pandas as pd
import pandas as np

def combine_mal_birth(mal_data, birth_data):
    #mal_data = pandas dataframe, information on diagnoses [TNRO, ICD9, ICD10]
    #birth_data = pandas dataframe, information of date [id, bdate,sex]
    #
    #Returns dataframe with date combined to diagnoses [id,date,icd9,icd10]
    mal_data.rename(columns = {mal_data.columns[0]: 'id'}, inplace=True)
    ret = pd.merge(birth_data, mal_data, how='right', on=['id']) #should be ['id', bdate, sex, ICD9, ICD10]
    
    #remove NaNs in diagnoses
    ret = ret.loc[(ret[ret.columns[3]].isna()==False) | (ret[ret.columns[4]].isna()==False)]
    
    #remove sex column
    ret = ret.drop(columns= ['sex']) #[id, bdate, icd9, icd10]
    
    #change column names to id and date
    ret.rename(columns={ret.columns[0]:'id', ret.columns[1]:'date'}, inplace=True)
    
    assert (ret['id'].dtype == np.dtype('float64')), "Date should be of type datetime64"
    assert (ret['date'].dtype == np.dtype('datetime64[ns]')), "Date should be of type datetime64"
    
    return(ret)
