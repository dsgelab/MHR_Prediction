# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 17:26:02 2020

@author: Atte
"""
import pandas as pd


def combine_diag_ped(diag, ped, cancer=0):
    #diag = dataframe containing [id, date, diag]
    #ped = dataframe containing [id, father_id, mother_id, sex, birth_year]
    #cancer = int, indicating if data comes from cancer file [id,date,age,diag]
    #
    #returns dataframe [id, date, age, father_id, mother_id, sex, diag]
    
    #combine dataframes on id -> result [id, date, diag, father_id, mother_id, sex, birth_year]
    ret = pd.merge(diag, ped, on='id') 
    
    if cancer == 0:
        #calculate age using date and birth_year and add it to dataframe and remove b_year
        age = ret[ret.columns[1]].map(lambda x: float(x.year)) - ret[ret.columns[-1]]
        ret.insert(2, 'age', age, True) # [id, date, age,diag, father_id, mother_id, sex, birth_year]
        
    ret = ret.drop(ret.columns[-1],axis=1) # [id, date, age,diag, father_id, mother_id, sex]
    
    #change order of columns
    diag = ret.pop(ret.columns[3])
    ret['diag'] =diag #[id, date, age, f_id, m_id, sex, diag]
    
    return(ret)