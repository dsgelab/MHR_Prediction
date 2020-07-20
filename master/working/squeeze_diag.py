# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 11:51:23 2020

@author: Atte
"""

def squeeze_diag(data, cancer=0):
    #data = pandas dataframe [id, date,diag1,diag2,...]
    #cancer = int, indicating if the file is from cancer dataset [id,date,age, diag1,...]
    #
    #Returns dataframe with ['id', 'date', 'diag'] or [id,date,age, diag]
    
    #take diagnoses to a list
    if cancer:
        temp = data[data.columns[3:]].values.tolist()
        data = data.loc[:,data.columns[0:3]]
        for i in range(len(temp)):
            temp[i] = [j for j in temp[i] if str(j) != 'None']
    else:
        temp = data[data.columns[2:]].values.tolist()
        data = data.loc[:,data.columns[0:2]]
        for i in range(len(temp)):
            temp[i] = [j for j in temp[i] if str(j) != 'nan']
    
    data['diag'] = temp
    return(data)

