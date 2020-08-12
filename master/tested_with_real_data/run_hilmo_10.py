# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 14:33:10 2020

@author: Atte
"""
import pandas as pd
import numpy as np
from extract_HILMO_10 import extract_HILMO_10
from squeeze_diag import squeeze_diag
from load_and_process_ped import load_and_process_ped
from combine_diag_ped import combine_diag_ped


#load all HILMO data and extract wanted info and squeeze diagnoses columns
li = ['TNRO','TUPVA','ICD10O_1','ICD10E_1','ICD10O_2','ICD10E_2','ICD10O_3','ICD10E_3','ICD10O_4','ICD10E_4',
'ICD10O_5','ICD10E_5','ICD10O_6','ICD10E_6','ICD10O_7','ICD10E_7','ICD10O_8','ICD10E_8','ICD10O_9','ICD10E_9',
'ICD10O_10','ICD10E_10','ICD10O_11','ICD10E_11','ICD10O_12','ICD10E_12','ICD10O_13','ICD10E_13','ICD10O_14','ICD10E_14',
'ICD10O_15','ICD10E_15','ICD10O_16','ICD10E_16','ICD10O_17','ICD10E_17','ICD10O_18','ICD10E_18','ICD10O_19','ICD10E_19',
'ICD10O_20','ICD10E_20','ICD10O_21','ICD10E_21','ICD10O_22','ICD10E_22','ICD10O_23','ICD10E_23','ICD10O_24','ICD10E_24',
'ICD10O_25','ICD10E_25','ICD10O_26','ICD10E_26','ICD10O_27','ICD10E_27','ICD10O_28','ICD10E_28','PITKADIAGO_1','PITKADIAGE_1',
'PITKADIAGO_2','PITKADIAGE_2','PITKADIAGO_3','PITKADIAGE_3','PITKADIAGO_4','PITKADIAGE_4','PITKADIAGO_5','PITKADIAGE_5',
'PITKADIAGO_6','PITKADIAGE_6','PITKADIAGO_7','PITKADIAGE_7','PITKADIAGO_8','PITKADIAGE_8','PITKADIAGO_9','PITKADIAGE_9',
'PITKADIAGO_10','PITKADIAGE_10','PITKADIAGO_11','PITKADIAGE_11','PITKADIAGO_12','PITKADIAGE_12','PITKADIAGO_13','PITKADIAGE_13',
'PITKADIAGO_14','PITKADIAGE_14','PITKADIAGO_15','PITKADIAGE_15','PITKADIAGO_16','PITKADIAGE_16','PITKADIAGO_17','PITKADIAGE_17',
'PITKADIAGO_18','PITKADIAGE_18','PITKADIAGO_19','PITKADIAGE_19','PITKADIAGO_20','PITKADIAGE_20','PITKADIAGO_21','PITKADIAGE_21',
'PITKADIAGO_22','PITKADIAGE_22','PITKADIAGO_23','PITKADIAGE_23','PITKADIAGO_24','PITKADIAGE_24','PITKADIAGO_25','PITKADIAGE_25',
'PITKADIAGO_26','PITKADIAGE_26','PITKADIAGO_27','PITKADIAGE_27','PITKADIAGO_28','PITKADIAGE_28','PITKADIAGO_29','PITKADIAGE_29',
'PITKADIAGO_30','PITKADIAGE_30','PITKADIAGO_31','PITKADIAGE_31','PITKADIAGO_32','PITKADIAGE_32','PITKADIAGO_33','PITKADIAGE_33']

data = pd.read_csv('/homes/aliu/DSGE_LRS/input/THL2019_804_hilmo_COMPLETE.csv', chunksize = 2650000, encoding='latin-1', usecols = li)

#load ped 
ped = load_and_process_ped("/homes/afohr/data/ped.csv") #[id, father_id, mother_id, sex, b_date]
bdate = pd.read_csv("/homes/afohr/data/bdate_sex.csv", parse_dates=[1]) # [id, bdate, sex]

for i, chunk in enumerate(data):
    diag = chunk
    diag = extract_HILMO_10(diag, li) # id, date, icd1- 28, pitkadiag1-33
    diag = squeeze_diag(diag) #id, date, diag
    #combine diags with pedigree info
    diag = combine_diag_ped(diag, ped, bdate) #[id, date, age, sex, f_id, m_id, diag]
    name = "/homes/afohr/data/Hilmo_10_ped_" + str(i) + ".csv"
    diag.to_csv(name, index=False)
