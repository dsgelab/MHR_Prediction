# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 13:47:05 2020

@author: Atte
"""

#birth = ['TNRO', 'LAPSEN_SYNTYMAPVM']

def extract_birth(data, list_of_cols):
    #data = pandas dataframe
    #list_of_cols = list of columns to be extracted e.g. ['TNRO', 'LAPSEN_SYNTYMAPVM']
    #
    #Returns dataframe with given columns, with only live birth included and rows with no diagnoses dropped
    ret = data[list_of_cols]
    
    #include only rows with date
    ret = ret.loc[ret[list_of_cols[1]].isna() == False]
    
    #change date to datetime64
    ret.loc[:,list_of_cols[1]] = ret[list_of_cols[1]].dt.normalize()
    
    return(ret)
