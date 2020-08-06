# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 11:51:23 2020

@author: Atte
"""

def squeeze_diag(data, cancer=0, non_diag_cols = 2):
    #data = pandas dataframe [id, date,diag1,diag2,...]
    #cancer = int, indicating if the file is from cancer dataset [id,date,age, sex,diag1,...]
    #non_diag_cols = int, indicating number of non diagnoses columns
    #
    #Returns dataframe with ['id', 'date', 'diag'] or [id,date,age, sex,diag]
    
    #take diagnoses to a list
    if cancer:
        #extract diagnoses on each row to a list
        temp = data[data.columns[non_diag_cols:]].values.tolist()
        #remove diagnoses rows
        data = data.loc[:,data.columns[0:4]]
        
        #remove missing values in diagnose lists
        for i in range(len(temp)):
            temp[i] = [j for j in temp[i] if str(j) != 'None']
        
        data.rename(columns= {data.columns[2]:'age'}, inplace=True) #[TNRO, TULOPV, age, sex]
    else:
        temp = data[data.columns[non_diag_cols:]].values.tolist()
        data = data.loc[:,data.columns[0:2]]
        for i in range(len(temp)):
            temp[i] = [j for j in temp[i] if str(j) != 'nan']
    
    data['diag'] = temp
    #change column names to id and date
    data.rename(columns= {data.columns[0]:'id', data.columns[1]:'date'}, inplace=True)
    return(data)

