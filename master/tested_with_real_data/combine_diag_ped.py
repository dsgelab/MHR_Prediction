# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 17:26:02 2020

@author: Atte
"""
import pandas as pd
import numpy as np


def combine_diag_ped(diag, ped, bdate_sex=None, cancer=0):
    #diag = dataframe containing [id, date, diag]
    #ped = dataframe containing [id, father_id, mother_id, sex, birth_date]
    #bdate_sex = dataframe containing [id, bdate, sex] More comprehendive than ped
    #cancer = int, indicating if data comes from cancer file [id, date, age, sex, diag]
    #
    #returns dataframe [id, date, age, father_id, mother_id, sex, diag]
    
    #drop sex and birth_date columns from ped
    ped = ped.drop(ped.columns[4], axis = 1)
    ped = ped.drop(ped.columns[3], axis = 1)
    
    #combine dataframes on id
    if cancer == 0:
        ret = pd.merge(diag, bdate_sex, how='left', on='id') #[id, date, diag, bdate, sex]
        ret = pd.merge(ret, ped,how='left', on='id') # [id, date, diag, bdate, sex, f_id, m_id]
        
        #calculate age using date and birth_date and add it to dataframe and remove b_date
        age = (ret[ret.columns[1]]-ret[ret.columns[3]]) / np.timedelta64(365, 'D')
        ret.insert(2, 'age', age, True) # [id, date, age, diag, bdate, sex, father_id, mother_id]
        ret = ret.drop(ret.columns[4],axis=1) # [id, date, age, diag, sex, father_id, mother_id]
        
        #change order of columns
        diag = ret.pop(ret.columns[3])
        ret['diag'] =diag #[id, date, age, sex, f_id, m_id, diag]
    
    if cancer == 1:
        ret = pd.merge(diag, ped,how='left', on='id') # [id, date,age, sex, diag, f_id, m_id]
        #change order of diag
        diag = ret.pop(ret.columns[4])
        ret['diag'] =diag # [id, date, age, sex, f_id, m_id, diag]
        
    
    return(ret)
