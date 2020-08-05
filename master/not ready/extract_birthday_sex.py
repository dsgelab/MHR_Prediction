# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 12:52:14 2020

@author: Atte
"""
import numpy as np
import pandas as pd

def extract_birthday_sex(data, id_col=None, rel_col=None, sex_col=None, bdate_col =None, t_format='%Y%m%d'):
    #data = dataframe
    #id_col = string. Name of id column
    #rel_col = string. Name of relationship column. Used for interpreting sex.
    #sex_col = string. Name of sex column
    #bdate_col = string. Name of birthdate column
    #t_format = string. Format of the date in data
    #
    #returns dataframe with given columns
    
    #take columns into list
    li = [id_col, bdate_col, rel_col, sex_col]
    li = [cols for cols in li if cols != None]
    
    #extract columns
    data= data[li].copy()
    
    #check if sex can be interpreted
    if sex_col == None and rel_col!=None:
        data['sex'] = data[rel_col].map(lambda x: 1 if x=='3i' else(2 if x=='3a' else np.nan))
        #remove rows with no info about sex and relationship column
        data = data[data.sex.isna() == False]
        data = data.drop(labels=[rel_col], axis = 1)
        #remove duplicates
        data = data.loc[data.duplicated() == False]
        assert (data.sex.dtype == np.dtype('float64')), "type of sex should be float64"
    
    #change birthdate to datetime64
    if bdate_col != None:
        data.loc[:,bdate_col] = pd.to_datetime(data[bdate_col], format = t_format).dt.normalize()
        data.rename(columns = {bdate_col:'bdate'}, inplace=True)
        assert (data['bdate'].dtype == np.dtype('datetime64[ns]')), "Date should be of type datetime64"
    
    #rename columns
    if sex_col != None:
        data.rename(columns = {id_col:'id', sex_col:'sex'}, inplace=True)
        assert (data.sex.dtype == np.dtype('float64')), "type of sex should be float64"
    else:
        data.rename(columns = {id_col:'id'}, inplace=True)
    
    data = data.loc[data.duplicated() == False]
    
    assert (data.id.dtype == np.dtype('float64')), "type of id should be float64"
    
    return(data)
