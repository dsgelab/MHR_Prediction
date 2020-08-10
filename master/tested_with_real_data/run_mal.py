# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 15:05:32 2020

@author: Atte
"""
import pandas as pd
import numpy as np
from extract_birth import extract_birth
from extract_mal import extract_mal
from combine_mal_birth import combine_mal_birth
from squeeze_diag import squeeze_diag
from combine_diag_ped import combine_diag_ped
from load_and_process_ped import load_and_process_ped

#load birth and malformation data and extract them 
bdate = pd.read_csv("/homes/afohr/data/bdate_sex.csv", parse_dates=[1]) # [id, bdate, sex]

mal = pd.read_sas('/homes/aliu/DSGE_LRS/input/anomalies_children_1987_2015_dg.sas7bdat', encoding='latin-1') 
li = ['TNRO','MANNER_OF_BIRTH', 'ICD9', 'ICD10']
mal = extract_mal(mal ,li) #[id, icd9, icd10]
mal2 = pd.read_sas('/homes/aliu/DSGE_LRS/input/anomalies_children_2016_dg.sas7bdat', encoding='latin-1')
mal2 = extract_mal(mal2, li)

#combine mals
mal = pd.concat([mal, mal2])

#combine birth and mal
mal = combine_mal_birth(mal, bdate) #[id, date,icd9, icd10]

#squeeze diags
mal = squeeze_diag(mal) #[id, date, diag]

#load ped 
ped = load_and_process_ped("/homes/afohr/data/ped.csv") #[id, father_id, mother_id, sex, b_date]

#combine mal diags with pedigree info
mal = combine_diag_ped(mal, ped, bdate) #[id, date, age, f_id, m_id, sex, diag]

mal.to_csv("/homes/afohr/data/mal_ped.csv", index=False)