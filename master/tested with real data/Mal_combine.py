# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 12:42:55 2020

@author: Atte
"""
import pandas as pd
#birth = ['TNRO', 'LAPSEN_SYNTYMAPVM'] #maybe 'RASKAUSNRO'
#mal = ['id', 'ICD9','ICD10'] #maybe 'RASKAUSNRO'

def combine_malformation_date(mal_data, birth_data):
    #mal_data = pandas dataframe, information on diagnoses
    #birth_data = pandas dataframe, information of date
    #
    #Returns dataframe with date combined to diagnoses
    ret = pd.merge(birth_data, mal_data, on=['TNRO']) #should be ['TNRO', DATE, ICD9,ICD10]
    
    #remove NaNs in diagnoses
    ret = ret.loc[(ret['ICD9'].isna()==False) | (ret['ICD10'].isna()==False)]
    
    #add in/outpatient column. no in/out info
    #ret.insert(2, 'In/Out', [1]*len(ret.index)) #should be ['TNRO', DATE, in/out, ICD9,ICD10]
    
    return(ret)
