# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 13:28:44 2020

@author: Atte
"""
import pandas as pd
import numpy as np
from extract_cancer import extract_cancer
from squeeze_diag import squeeze_diag
from combine_diag_ped import combine_diag_ped
from load_and_process_ped import load_and_process_ped

#load cancer data and extract them 
cancer = pd.read_csv('/homes/aliu/DSGE_LRS/input/fcr_all_data.csv',encoding='UTF-8', sep=';', parse_dates=['dg_date'])
li_c = ['TNRO', 'dg_date', 'dg_age', 'morpho', 'topo','cancertype_icd10']
cancer = extract_cancer(cancer, li_c) #[id, date, age, morpho, topo, diag-10]

#squeeze diags
cancer = squeeze_diag(cancer, cancer=1) #[id, date, age, diag]

#load ped 
ped = load_and_process_ped("/homes/afohr/data/ped.csv") #[id, father_id, mother_id, sex, b_date]

#combine cancer diags with pedigree info
cancer = combine_diag_ped(cancer, ped, cancer=1) #[id, date, age, f_id, m_id, sex, diag]

cancer.to_csv("/homes/afohr/data/cancer_ped.csv", index=False)