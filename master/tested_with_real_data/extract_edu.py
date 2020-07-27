# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 12:39:40 2020

@author: Atte
"""

def extract_edu(data, list_of_cols):
    #data = pandas dataframe
    #list_of_cols = list of columns to be extracted e.g. ['TNRO', 'vuosi', 'iscfi2013', 'kaste_t2']
    #
    #Returns dataframe with given columns, where rows with no year info are dropped
    ret = data[list_of_cols]
    
    #remove rows with no yearly info
    ret = ret.dropna(subset=[ret.columns[1]])
    
    #change NaNs in kaste to 91 = unknown
    ret[ret.columns[3]] = ret[ret.columns[3]].fillna(91)
    #And Nans in iscfi2013 to 99
    ret[ret.columns[2]] = ret[ret.columns[2]].fillna(99)
    
    return(ret)
