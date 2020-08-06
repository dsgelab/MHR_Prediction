# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 15:40:45 2020

@author: Atte
"""
#Please use list_of_cols in form ['TNRO','TUPVA', 'diag1',...,'diag_n']
def extract_HILMO_8_9(data, list_of_cols, icd):
    #data = pandas dataframe
    #list_of_cols = list of columns to be extracted e.g. ['id', 'arrival', 'diag_1',..., 'diag_n']
    #icd = string of icd code used in original file e.g. 'icd8' or 'icd9'
    #
    #Returns dataframe with given columns, where diagnoses are limited to 3 characters & rows
    #with no diagnoses are removed. [TNRO, arrival, diag1,...,diagn]
    ret = data[list_of_cols]
    
    #remove rows with nans in main diagnose
    ret = ret.dropna(subset=[list_of_cols[2]])
    
    #remove last numbers from diagnoses, add icd prefix and change column name. 
    for i in range(2,len(list_of_cols)):
        ret[list_of_cols[i]] = ret[list_of_cols[i]].map(lambda x: icd + '-' + str(x[:3]), na_action='ignore')
        
    return(ret)
