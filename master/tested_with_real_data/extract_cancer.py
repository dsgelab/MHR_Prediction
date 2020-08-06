# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 13:56:14 2020

@author: Atte
"""
import pandas as pd
import numpy as np
#li = ['TNRO', 'dg_date', 'dg_age', 'sex','morpho', 'topography', 'cancertype_icd10']

def extract_cancer(data, id_col=None, date_col=None, age_col=None, sex_col=None, diag_cols=None):
    #data = pandas dataframe
    #id_col = string. Name of id column
    #date_col = string. Name of date column
    #age_col = string. Name of age column
    #sex_col = string. Name of sex column
    #diag_cols = list of strings. Names of diagnose columns
    #
    #Returns dataframe with ['TNRO', 'dg_date', 'dg_age', 'sex','morpho', 'topography', 'diag1', 'diag2']
    if id_col==None:
        return(print("Add column for patient ids"))
    
    #take columns into list
    if isinstance(diag_cols, list)==False:
        list_of_cols = [id_col, date_col, age_col, sex_col, diag_cols]
        
    elif isinstance(diag_cols, list)==True:
        list_of_cols = [id_col, date_col, age_col, sex_col] + diag_cols
        
    list_of_cols = [cols for cols in list_of_cols if cols != None]
    
    ret = data[list_of_cols].copy()
    
    #cancertype_icd10 contains diagnoses like C01,C02,C03 -> need to extract them separately
    diag = ret[diag_cols[-1]].str.split(pat=',', expand=True) #makes a df with diagnoses
    ret = pd.concat([ret,diag], axis=1)
    ret = ret.drop([diag_cols[-1]], axis=1) #drops 'cancertype_icd10'
    
    #calculate how many columns have been given and shere the for loop should start
    start_index = 2 + len([cols for cols in [id_col, date_col, age_col, sex_col] if cols != None]) 
    
    #add icd prefix. ret should be ['TNRO', 'dg_date', 'dg_age', 'sex','morpho','topo','diag1',...,'diag_n'] if all cols given
    for i in range(start_index, len(ret.columns)):
        ret[ret.columns[i]] = ret[ret.columns[i]].map(lambda x: '10-' + str(x[:3]), na_action='ignore')
    
    #add prefixes for morphology and topography
    ret[diag_cols[0]] = ret[diag_cols[0]].map(lambda x:'m-' + str(x), na_action='ignore')
    ret[diag_cols[1]] = ret[diag_cols[1]].map(lambda x:'t-' + str(x), na_action='ignore')
    
    #change gender to same format as in pedigree file
    if sex_col!=None:
        ret[sex_col] = ret[sex_col].map(lambda x: int(x) +1)
    
    #change types
    ret = ret.astype({id_col : np.dtype('float64')})
    assert (ret[id_col].dtype == np.dtype('float64')), "type of id should be float64"
    
    if date_col != None:
        assert (ret[date_col].dtype == np.dtype('datetime64[ns]')), "Date should be of type datetime64"
    if age_col != None:
        ret[age_col] = ret[age_col].str.replace(',', '.')
        ret = ret.astype({age_col : np.dtype('float64')})
        assert (ret[age_col].dtype == np.dtype('float64')), "type of id should be float64"
    if sex_col != None:
        ret = ret.astype({sex_col : np.dtype('float64')})
        assert (ret[sex_col].dtype == np.dtype('float64')), "type of id should be float64"
    
    return(ret)
