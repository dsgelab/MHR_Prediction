    # -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 10:32:34 2020

@author: Atte
"""
import pandas as pd


def extract_HILMO_10(data, list_of_cols):
    #data = pandas dataframe
    #list_of_cols = list of columns to be extracted e.g. ['id', 'arrival', ('in/out',) diag_1',..., 'diag_n']
    #
    #Returns dataframe with given columns, where diagnoses are limited to 3 characters & rows
    #with no diagnoses are removed.
    ret = data[list_of_cols]
    
    #remove rows with nans in main diagnose
    ret = ret.dropna(subset=[list_of_cols[2]])
    
    #Change in/outpatient encoding. No info on in/outpatient
    #ret.loc[ret[list_of_cols[2]] <= 10, ret[list_of_cols[2]]] = 1
    #ret.loc[ret[list_of_cols[2]] > 10, ret[list_of_cols[2]]] = 0
    
    #remove last numbers from diagnoses and add icd prefix. 
    for i in range(2,len(list_of_cols)):
        ret[list_of_cols[i]] = ret[list_of_cols[i]].map(lambda x: '10-' + str(x[:3]), na_action='ignore')
    
    #change arrival to datetime64
    ret.loc[:,list_of_cols[1]] = pd.to_datetime(ret[ret.columns[1]], format='%d%b%Y:%H:%M:%S').dt.normalize()
    
    return(ret)
