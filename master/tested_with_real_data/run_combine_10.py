# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 10:18:06 2020

@author: Atte
"""
import pandas as pd

data = pd.read_csv('/homes/afohr/data/Hilmo_10_ped_0.csv', parse_dates=[1])

for i in range(1,41):
    name = '/homes/afohr/data/Hilmo_10_ped_' + str(i) + '.csv'
    data = pd.concat([data, pd.read_csv(name, parse_dates=[1])])

data.to_csv('/homes/afohr/data/Hilmo_10_ped_all.csv', index=False)