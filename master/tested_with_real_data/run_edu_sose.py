# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 13:19:47 2020

@author: Atte
"""
import pandas as pd
import numpy as np
from extract_edu import extract_edu
from extract_sose import extract_sose
from combine_sose_edu import combine_sose_edu


#load education data and combine them 
edu = pd.read_sas('/homes/aliu/DSGE_LRS/input/koulutus_ala_aste_u1477_al.sas7bdat', encoding='latin-1')
edu2 = pd.read_sas('/homes/aliu/DSGE_LRS/input/koulutus_ala_aste_u1477_a.sas7bdat', chunksize= 2000000, encoding='latin-1')

for i, chunk in enumerate(edu2):
    edu = pd.concat([edu, chunk])


#extract wanted information
edu = extract_edu(edu, id_col='TNRO', year_col='vuosi', iscfi2013_col = 'iscfi2013', kaste_col='kaste_t2') # [id, year, iscfi, kaste]

#load socio-economic data and extract wanted information
data_sose = pd.read_csv('/homes/afohr/data/socio_income.csv', chunksize=2000000)
columns = ['TNRO','vuosi', 'sose', 'Eur']
sose = pd.DataFrame(columns=columns)
for i, chunk in enumerate(data_sose):
    sose = pd.concat([sose, extract_sose(chunk, id_col='TNRO', year_col='vuosi', sose_col='sose',income_col='Eur', text_col='Text')])

#combine both of the files
edu = combine_sose_edu(sose, edu) #['TNRO', vuosi, sose, income, iscfi2013,kaste_t2]

edu.to_csv("/homes/afohr/data/sose_edu.csv", index=False)