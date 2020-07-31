# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 17:26:02 2020

@author: Atte
"""
import pandas as pd
import numpy as np


def combine_diag_ped(diag, ped, cancer=0):
    #diag = dataframe containing [id, date, diag]
    #ped = dataframe containing [id, father_id, mother_id, sex, birth_date]
    #cancer = int, indicating if data comes from cancer file [id, date, age, sex, diag]
    #
    #returns dataframe [id, date, age, father_id, mother_id, sex, diag]
    
    #combine dataframes on id -> result [id, date, diag, father_id, mother_id, sex, birth_year]
    if cancer == 0:
        ret = pd.merge(diag, ped,how='left', on='id') # [id, date, diag, f_id, m_id, sex, birth_date]
        #calculate age using date and birth_date and add it to dataframe and remove b_date
        age = (ret[ret.columns[1]]-ret[ret.columns[-1]]) / np.timedelta64(365, 'D')
        ret.insert(2, 'age', age, True) # [id, date, age,diag, father_id, mother_id, sex, birth_year]
        ret = ret.drop(ret.columns[-1],axis=1) # [id, date, age,diag, father_id, mother_id, sex]
        #change order of columns
        diag = ret.pop(ret.columns[3])
        ret['diag'] =diag #[id, date, age, f_id, m_id, sex, diag]
    
    if cancer == 1:
        #drop sex and birth_date columns from ped
        ped = ped.drop(ped.columns[-1], axis = 1)
        ped = ped.drop(ped.columns[3], axis = 1)
        ret = pd.merge(diag, ped,how='left', on='id') # [id, date,age, sex, diag, f_id, m_id]
        #change order
        sex = ret.pop(ret.columns[3])
        ret['sex'] = sex # [id, date, age, diag, f_id, m_id, sex]
        diag = ret.pop(ret.columns[3])
        ret['diag'] =diag # [id, date, age, f_id, m_id, sex, diag]
        
    
    return(ret)
