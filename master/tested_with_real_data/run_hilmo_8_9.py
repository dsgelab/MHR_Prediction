# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 13:43:44 2020

@author: Atte
"""
import pandas as pd
import numpy as np
from extract_HILMO_8_9 import extract_HILMO_8_9
from squeeze_diag import squeeze_diag
from load_and_process_ped import load_and_process_ped
from combine_diag_ped import combine_diag_ped


#load all HILMO 8 and 9 data and extract wanted info and squeeze diagnoses columns
H_8 = pd.read_sas('/homes/aliu/DSGE_LRS/input/thl2019_804_poisto_6986_COMPLETE.sas7bdat', encoding='UTF-8')
li_8 = li=['TNRO','TULOPV','DG1','DG2','DG3','DG4']
H_8 = extract_HILMO_8_9(H_8, li_8, '8') #[TNRO,TULOPV,dg1-4]
H_8 = squeeze_diag(H_8) #[id, date, diag]

H_91 = pd.read_sas('/homes/aliu/DSGE_LRS/input/thl2019_804_poisto_8793_COMPLETE.sas7bdat', encoding='UTF-8')
li_91 = ['TNRO','TUPVA','PDG','SDG1','SDG2','SDG3']
H_91 = extract_HILMO_8_9(H_91, li_91, '9')
H_91 = squeeze_diag(H_91) #[id, date, diag]

H_92 = pd.read_sas('/homes/aliu/DSGE_LRS/input/thl2019_804_hilmo_9495_COMPLETE.sas7bdat', encoding='UTF-8')
li_92 = ['TNRO','TUPVA','PDG','SDG1','TUTAP']
H_92 = extract_HILMO_8_9(H_92, li_92, '9')
H_92 = squeeze_diag(H_92) #[id, date, diag]

#concatenate all data
H_8 = pd.concat([H_8, H_91, H_92])

#load ped 
ped = load_and_process_ped("/homes/afohr/data/ped.csv") #[id, father_id, mother_id, sex, b_date]

#combine death diags with pedigree info
H_8 = combine_diag_ped(H_8, ped) #[id, date, age, f_id, m_id, sex, diag]

H_8.to_csv("/homes/afohr/data/Hilmo_8_9_ped.csv", index=False)