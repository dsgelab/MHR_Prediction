# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 13:17:28 2020

@author: Atte
"""
import pandas as pd
#li = ['TNRO','kuolpvm','kvuosi','tpks','vks','m1','m2','m3','m4']

def extract_death(data, list_of_cols):
    #data = pandas dataframe
    #list_of_cols = list of columns to be extracted e.g. ['id', 'arrival', 'diag_1',..., 'diag_n']
    #
    #Returns dataframe with given columns, where diagnoses are limited to 3 characters & rows
    #with no diagnoses are removed. [TNRO, arrival, in/out, diagnoses]
    ret = data.loc[:,list_of_cols]
    
    #remove rows with nans in main diagnose
    ret = ret.dropna(subset=[list_of_cols[3]])
    
    #separate by year of death
    icd8 = ret.loc[ret[list_of_cols[2]] <=1986].copy()
    icd9 = ret.loc[(1986 < ret[list_of_cols[2]]) & (ret[list_of_cols[2]] <1996)].copy()
    icd10 = ret.loc[ret[list_of_cols[2]] >= 1996].copy()
    
    #remove last numbers from diagnoses and add icd prefix. 
    for i in range(3,len(list_of_cols)):
        icd8.loc[:,list_of_cols[i]] = icd8.loc[:,list_of_cols[i]].map(lambda x:  '9-' + str(x[:3]) if x[-1].isalpha()==True else '8-' + str(x[:3]), na_action='ignore')
        icd9.loc[:,list_of_cols[i]] = icd9.loc[:,list_of_cols[i]].map(lambda x:  '9-' + str(x[:3]) if x[-1].isalpha()==True else ('10-' + str(x[:3]) if x[0].isalpha() else '8-' + str(x[:3])), na_action='ignore')
        icd10.loc[:,list_of_cols[i]] = icd10.loc[:,list_of_cols[i]].map(lambda x:  '9-' + str(x[:3]) if x[-1].isalpha()==True else '10-' + str(x[:3]), na_action='ignore')
    
    #combine the temporary dataframes
    ret.loc[:,:] = pd.concat([icd8, icd9, icd10])
    ret = ret.drop(list_of_cols[2], axis =1)
    
    #change kuolpvm to datetime64
    ret.loc[:,list_of_cols[1]] = pd.to_datetime(ret[ret.columns[1]], format = '%Y%m%d')
    
    #insert new column indicating inpatient. no in/out info
    #ret.insert(2, 'In/Out', [1]*len(ret.index))
    
    return(ret)
