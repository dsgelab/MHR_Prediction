# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 15:44:02 2020

@author: Atte
"""


def combine_socio_diag(socio_data, diag_data):
    #socio_data = pandas dataframe, information on sociodemographics ['TNRO', vuosi, sose, kaste_t2]
    #diag_data = pandas dataframe, information of diagnoses ['TNRO', 'vuosi', 'date', 'in/out', diag_1',..., 'diag_n']
    #
    #Returns dataframe with sociodemographics combined to diagnoses
    raise Exception('not ready')
    
    ret = pd.merge(socio_data, diag_data, on=['TNRO', 'vuosi']) 
    #should be ['TNRO','vuosi','sose','edu',DATE,in/out,diag1,...,diag_n]
    
    #remove NaNs in main diagnoses
    ret = ret.dropna(subset=[ret.columns[6]])
    
    return(ret)