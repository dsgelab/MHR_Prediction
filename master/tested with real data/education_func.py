# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 12:39:40 2020

@author: Atte
"""

def extract_education(data):
    #data = pandas dataframe
    #list_of_cols = list of columns to be extracted e.g. ['TNRO', 'vuosi', 'kaste_t2']
    #
    #Returns dataframe with given columns, where rows with no year info are dropped
    
    
    #remove rows with no yearly info
    data = data.dropna(subset=[data.columns[1]])
    
    #change NaNs in sose to 91 = unknown
    data[data.columns[3]].fillna(91)
    
    return(data)
