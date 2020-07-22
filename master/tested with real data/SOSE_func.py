# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 12:19:27 2020

@author: Atte
"""

def extract_sose(data, list_of_cols):
    #data = pandas dataframe
    #list_of_cols = list of columns to be extracted e.g. ['TNRO', 'vuosi', 'sose']
    #
    #Returns dataframe with given columns, where rows with no year info are dropped
    ret = data[list_of_cols]
    
    #remove rows with no yearly info
    ret = ret.dropna(subset=[list_of_cols[1]])
    
    #change NaNs in sose to 99 = unknown
    ret[list_of_cols[2]] = ret[list_of_cols[2]].fillna(99)
    
    return(ret)
    