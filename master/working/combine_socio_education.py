# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 15:44:43 2020

@author: Atte
"""

def combine_sose_edu(sose_data, edu_data):
    #sose_data = pandas dataframe, information on sosioeconomic status ['TNRO', 'vuosi', 'sose']
    #education_data = pandas dataframe, information of education ['TNRO', 'vuosi', 'kaste_t2']
    #
    #Returns dataframe with sosieconomic status combined with education given a year
    ret = pd.merge(sose_data, edu_data, on=['TNRO', 'vuosi']) #should be ['TNRO', vuosi, sose, kaste_t2]
    
    return(ret)