# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 15:44:43 2020

@author: Atte
"""
import pandas as pd

def combine_sose_edu(sose_data, edu_data):
    #sose_data = pandas dataframe, information on sosioeconomic status ['TNRO', 'vuosi', 'sose']
    #education_data = pandas dataframe, information of education ['TNRO', 'vuosi', 'iscfi2013','kaste_t2']
    #
    #Returns dataframe with sosieconomic status combined with education given a year
    #ret = dataframe with columns [id, year, sose, iscfi2013,kaste_t2]
    ret = pd.merge(sose_data, edu_data, how ='outer', on=['TNRO', 'vuosi']) #should be ['TNRO', vuosi, sose, iscfi2013,kaste_t2]
    
    #change column names to id and year
    ret.rename(columns={ret.columns[0]:'id', ret.columns[1]:'year'}, inplace=True)
    
    return(ret)
