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
edu1 = pd.read_sas('/homes/aliu/DSGE_LRS/input/koulutus_ala_aste_u1477_al.sas7bdat', encoding='latin-1')
edu2 = pd.read_sas('/homes/aliu/DSGE_LRS/input/koulutus_ala_aste_u1477_a.sas7bdat', encoding='latin-1')
edu2 = pd.concat([edu1, edu2])

#extract wanted information
edu2 = extract_edu(edu2)

#load socio-economic data and extract wanted information
sose = pd.read_sas('/homes/aliu/DSGE_LRS/input/sose_u1477_a.sas7bdat', encoding='UTF-8')
li = ['TNRO', 'vuosi', 'sose']
sose = extract_sose(sose, li)

#combine both of the files
edu2 = combine_sose_edu(sose, edu2)

edu2.to_csv("/homes/afohr/data/sose_edu.csv", index=False)