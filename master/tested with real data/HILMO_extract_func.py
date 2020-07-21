# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 15:40:45 2020

@author: Atte
"""
#Please use list_of_cols in form ['TNRO','TUPVA', 'diag1',...,'diag_n']
def extract_diagnoses(data, list_of_cols, icd):
    #data = pandas dataframe
    #list_of_cols = list of columns to be extracted e.g. ['id', 'arrival', 'diag_1',..., 'diag_n']
    #icd = string of icd code used in original file e.g. 'icd8' or 'icd9'
    #
    #Returns dataframe with given columns, where diagnoses are limited to 3 characters & rows
    #with no diagnoses are removed. [TNRO, arrival, (in/out,) diagnoses]
    ret = data[list_of_cols]
    
    #remove rows with nans in main diagnose
    ret = ret.dropna(subset=[list_of_cols[2]])
    
    #remove last numbers from diagnoses, add icd prefix and change column name. 
    #diag_number = 1
    for i in range(2,len(list_of_cols)):
        ret[list_of_cols[i]] = ret[list_of_cols[i]].map(lambda x: icd + '-' + str(x[:3]), na_action='ignore')
        #name = 'diag' + str(diag_number)
        #ret.rename(columns= {list_of_cols[i]:name}, inplace=True)
        #diag_number +=1
    
    #insert new column indicating inpatient. no in/out info
    #ret.insert(2, 'In/Out', [1]*len(ret.index))
    
    #rename id and date
    #ret.rename(columns= {list_of_cols[0]:'id', list_of_cols[1]:'date'}, inplace=True)
    
    return(ret)
