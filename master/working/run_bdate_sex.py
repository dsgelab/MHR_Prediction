# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 14:54:00 2020

@author: Atte
"""
import pandas as pd
import numpy as np
from extract_birthday_sex import extract_birthday_sex

data = pd.read_sas('/homes/aliu/DSGE_LRS/input/thl2019_804_tutkhenk.sas7bdat', chunksize = 2650000, encoding='latin-1')

columns = ['id','bdate', 'sex']
df = pd.DataFrame(columns=columns)
for i, chunk in enumerate(data):
    df = pd.concat([df, extract_birthday_sex(chunk, id_col= 'SUKULAISEN_TNRO', sex_col='SUKUPUOLI', bdate_col='SUKULAISEN_SYNTYMAPV')])
    #remove duplicates
    df = df.loc[df.duplicated() == False]

data = pd.read_sas('/homes/aliu/DSGE_LRS/input/thl2019_804_tljslv.sas7bdat', chunksize = 2650000, encoding='latin-1')

for i, chunk in enumerate(data):
    df = pd.concat([df, extract_birthday_sex(chunk, id_col= 'SUKULAISEN_TNRO', sex_col='SUKUPUOLI', bdate_col='SUKULAISEN_SYNTYMAPV')])
    #remove duplicates
    df = df.loc[df.duplicated() == False]


df.to_csv("/homes/afohr/data/bdate_sex.csv", index=False)