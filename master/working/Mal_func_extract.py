# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 10:52:02 2020

@author: Atte
"""



def extract_malformation(data, list_of_cols):
    #data = pandas dataframe
    #list_of_cols = list of columns to be extracted e.g. ['id', 'MANNER_OF_BIRTH', 'ICD9','ICD10']
    #
    #Returns dataframe with given columns, with only live birth included and rows with no diagnoses dropped
    ret = data[list_of_cols]
    
    #include only rows with live birth and remove MANNER_OF_BIRTH column
    ret = ret.loc[ret[ret.columns[1]] == 1]
    ret = ret.drop([list_of_cols[1]], axis=1)
    
    #prefix icd9 and 10
    ret[ret.columns[1]] = ret[ret.columns[1]].map(lambda x: '9-' + str(x[:3]), na_action='ignore')
    ret[ret.columns[2]] = ret[ret.columns[2]].map(lambda x: '10-' + str(x[:3]), na_action='ignore')
    
    #remove rows with no diagnoses
    ret = ret.loc[(ret[ret.columns[1]].isna()==False) | (ret[ret.columns[2]].isna()==False)]
    #one way could be to check if has icd10-> remove icd9. if not icd10->take icd9
    
    return(ret)
