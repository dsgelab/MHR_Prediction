# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 10:13:43 2020

@author: Atte
"""
import pandas as pd

def load_and_process_ped(folder):
    #ped = dataframe [id, father_id, mother_id, sex, b_date]
    #folder = string of path to ped csv
    ped = pd.read_csv(folder, encoding='UTF-8')
    
    
    #drop rows with nans in id
    ped = ped.dropna(subset=[ped.columns[0]])
    
    #change to datetime64
    ped.b_date = ped.b_date.map(lambda x: str(int(x)))
    ped.b_date = pd.to_datetime(ped.b_date, format='%Y%m%d', errors='coerce')
    
    return(ped)
