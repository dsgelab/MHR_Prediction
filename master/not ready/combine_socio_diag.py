# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 15:44:02 2020

@author: Atte
"""
import pandas as pd


def combine_socio_diag(socio_data, diag_data):
    #socio_data = pandas dataframe, information on sociodemographics [id, year, sose, iscfi,kaste_t2]
    #diag_data = pandas dataframe, [id, date, age, father_id, mother_id, sex, diag]
    #
    #ret =dataframe with columns  [id, date, age, father_id, mother_id, sex, sose, iscfi, kaste, diag]
    
    #make new column with year info
    diag_data['year'] = diag_data[diag_data.columns[1]].map(lambda x: x.year)
    
    ret = pd.merge(diag_data, socio_data, how= 'left',on=['id', 'year']) 
    #should be [id, date, age, f_id, m_id, sex, diag, year, sose, iscfi, kaste]
    #drop year
    ret = ret.drop(labels= ret.columns[7], axis=1)
    
    diag = ret.pop(ret.columns[6])
    ret['diag'] =diag #[id, date, age, f_id, m_id, sex, sose, iscfi, kaste, diag]
    return(ret)
