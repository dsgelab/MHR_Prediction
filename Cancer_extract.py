# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 13:56:14 2020

@author: Atte
"""

def cancer_extract(data, list_of_cols):
    #data = pandas dataframe
    #list_of_cols = list of columns to be extracted e.g. ['TNRO', 'dg_date', 'dg_age','morpho', 'topography', 'cancertype_icd10']
    #
    #Returns dataframe with ['TNRO', 'dg_date', 'dg_age', 'diag1', 'diag2']
    ret = data[list_of_cols]
    
    #remove rows with nans in diagnose. data is complete
    #ret = ret.dropna(subset=[list_of_cols[3]])
    
    #cancertype_icd10 contains diagnoses like C01,C02,C03 -> need to extract them separately
    diag = ret[list_of_cols[5]].str.split(pat=',', expand=True) #makes a df with diagnoses
    ret = pd.concat([ret,diag], axis=1)
    ret = ret.drop([list_of_cols[5]], axis=1) #drops 'cancertype_icd10'
    
    #add icd prefix. ret should be ['TNRO', 'dg_date', 'dg_age','morpho','topo','diag1',...,'diag_n']
    for i in range(5,len(ret.columns)):
        ret[ret.columns[i]] = ret[ret.columns[i]].map(lambda x: '10-' + str(x), na_action='ignore')
    
    #add prefixes for morphology and topography
    ret[ret.columns[3]] = ret[ret.columns[3]].map(lambda x:'m-' + str(x), na_action='ignore')
    ret[ret.columns[4]] = ret[ret.columns[4]].map(lambda x:'t-' + str(x), na_action='ignore')
    
    
    #add in/outpatient encoding. no in/out info
    #ret.insert(2, 'In/Out', [1]*len(ret.index)) #should be ['TNRO', 'dg_date', 'in/out','dg_age', 'diag1',..., 'diag_n']
    
    
    
    return(ret)

