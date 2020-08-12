# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 12:19:27 2020

@author: Atte
"""
#['TNRO', 'vuosi', 'sose', 'Eur]
import numpy as np

def extract_sose(data, id_col=None, year_col=None, sose_col=None, income_col =None, text_col = None):
    #data = pandas dataframe
    #id_col = string. Name of id column
    #year_col = string. Name of year column
    #sose_col = string. Name of sose column
    #income_col = string. Name of income column
    #text_col = string. Name of text column that includes the description of profession. Used if old
    #           sose codes are not converted to new ones
    #
    #Returns dataframe with given columns, where rows with no year info are dropped
    if id_col == None or year_col==None:
        return(print("Add column for patient ids or year"))
    
    li = [id_col, year_col, sose_col, income_col, text_col]
    li = [cols for cols in li if cols != None]
    
    ret = data[li]
    
    #remove rows with no yearly info
    ret = ret.dropna(subset=[year_col])
    
    if sose_col!=None:
        #change NaNs in sose to 99 = unknown
        ret[sose_col] = ret[sose_col].fillna(99)
        if text_col != None:
            #change old pensioner and student sose codes to new ones
            ret.loc[ret[text_col] == 'Pensioners (in later classification 70)' , sose_col] = 70
            ret.loc[ret[text_col] == 'Students (in later classification 60)' , sose_col] = 60
            ret.drop([text_col], axis = 1, inplace = True)
        #change old classification to new ones. More info SCE_FIN.pdf at Drive DSGE_LRS/Finland
        ret.loc[ret[sose_col] == 59 , sose_col] = 99
        ret.loc[ret[sose_col] == 82 , sose_col] = 99
        ret.loc[ret[sose_col] == 91 , sose_col] = 81
        ret.loc[ret[sose_col] == 92 , sose_col] = 99
        ret.loc[ret[sose_col] == 93 , sose_col] = 81
        #add prefix
        ret[sose_col] = ret[sose_col].map(lambda x: 'sose-' + str(x), na_action='ignore')
    
    if income_col != None:
        assert (ret[income_col].dtype == np.dtype('float64')), "type of id should be float64"
    
    return(ret)
