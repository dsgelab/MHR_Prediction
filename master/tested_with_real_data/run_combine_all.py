# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 11:55:31 2020

@author: Atte
"""
import pandas as pd

hilmo10 = pd.read_csv('/homes/afohr/data/Hilmo_10_ped_all.csv', parse_dates=[1])
hilmo89 = pd.read_csv('/homes/afohr/data/Hilmo_8_9_ped.csv', parse_dates=[1])
cancer = pd.read_csv('/homes/afohr/data/cancer_ped.csv', parse_dates=[1])
death = pd.read_csv('/homes/afohr/data/death_ped.csv', parse_dates=[1])
mal = pd.read_csv('/homes/afohr/data/mal_ped.csv', parse_dates=[1])

hilmo10 = pd.concat([hilmo10, hilmo89, cancer, death, mal])

hilmo10 = hilmo10.sort_values(['id', 'date'])

hilmo10.to_csv("/homes/afohr/data/diag_ped.csv", index=False)
