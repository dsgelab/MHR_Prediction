# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 16:19:04 2020

@author: Atte
"""
import pandas as pd
import numpy as np
from extract_death import extract_death
from squeeze_diag import squeeze_diag
from load_and_process_ped import load_and_process_ped
from combine_diag_ped import combine_diag_ped


#load death data and extract them 
death = pd.read_sas('/homes/aliu/DSGE_LRS/input/kuolemansyyt_u1477_a.sas7bdat', encoding='latin-1')
li = ['TNRO','kuolpvm','kvuosi','tpks','vks','m1','m2','m3','m4']
death = extract_death(death, li) #[id,date,tpks, vks, m1-4]

#squeeze diags
death = squeeze_diag(death) #[id, date, diag]

#load ped 
ped = load_and_process_ped("/homes/afohr/data/ped.csv") #[id, father_id, mother_id, sex, b_date]

#combine death diags with pedigree info
death = combine_diag_ped(death, ped) #[id, date, age, f_id, m_id, sex, diag]

death.to_csv("/homes/afohr/data/death_ped.csv", index=False)