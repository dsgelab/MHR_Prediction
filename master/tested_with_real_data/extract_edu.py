# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 12:39:40 2020

@author: Atte
"""

def extract_edu(data,  id_col=None, year_col=None, iscfi2013_col = None, kaste_col=None):
    #data = pandas dataframe
    #id_col = string. Name of id column
    #year_col = string. Name of year column
    #iscfi2013_col = string. Name of class column
    #
    #Returns dataframe with given columns, where rows with no year info are dropped
    if id_col == None:
        return(print("Add column for patient ids"))
    
    list_of_cols = [id_col, year_col, iscfi2013_col, kaste_col]
    
    ret = data[list_of_cols]
    
    if year_col != None:
        #remove rows with no yearly info
        ret = ret.dropna(subset=[ret.columns[1]])
    
    if kaste_col != None:
        #change NaNs in kaste to 91 = unknown
        ret[kaste_col] = ret[kaste_col].fillna(91)
        ret[kaste_col] = ret[kaste_col].map(lambda x: "kaste-" +str(x), na_action='ignore')
    
    if iscfi2013_col != None:
        #And Nans in iscfi2013 to 99
        ret[iscfi2013_col] = ret[iscfi2013_col].fillna(99)
        ret[iscfi2013_col] = ret[iscfi2013_col].map(lambda x: "iscfi-" +str(x), na_action='ignore')
    
    return(ret)
