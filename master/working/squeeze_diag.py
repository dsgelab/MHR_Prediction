# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 11:51:23 2020

@author: Atte
"""

def squeeze_diag(data, list_of_diag):
    #data = pandas dataframe
    #list_of_diag = list of diagnoses to be extracted e.g. ['diag1','diag2','diag3']
    #
    #Returns dataframe with ['TNRO', 'dg_date', 'diag']
    temp = data[data.columns[2:]].values.tolist()
    data = data.loc[:,'id':'date']
    for i in range(len(temp)):
        temp[i] = [j for j in temp[i] if str(j) != 'nan']

    data['diag'] = temp
    return(data)

