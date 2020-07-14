# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 11:51:23 2020

@author: Atte
"""

def squeeze_diag(data):
    #data = pandas dataframe [id, date,diag1,diag2,...]
    #list_of_diag = list of diagnoses to be extracted e.g. ['diag1','diag2','diag3']
    #
    #Returns dataframe with ['TNRO', 'dg_date', 'diag']
    temp = data[data.columns[2:]].values.tolist()
    data = data.loc[:,data.columns[0:2]]
    for i in range(len(temp)):
        temp[i] = [j for j in temp[i] if str(j) != 'nan']

    data['diag'] = temp
    return(data)

