# Documentation

## Extracting data
**Example 1.** Once you have loaded data from atlas, you can extract the wanted columns from that data. Lets use Socio-economic data as an example.
```
data = extract_sose(data, ['TNRO', 'vuosi', 'sose'])
```
This will extract the columns that are listed in the second input. The list is order specific. It will also do some preprocessing, such as remove rows with no yearly info and change NaN values to a number corresponding unknown value. The other extract function work similarly. 

## Combining DataFrames
**Example 2.** There are functions for combining DataFrames. These can be used to ultimately get a DataFrame that has information about the patients visits, such as [id, date, age, father_id, mother_id, sex, sose (socio-economic status), iscfi2013 (education orientation), kaste_t2(level of education), diagnoses]. (Note that sose will change into average income given visits year, socio-economic group and sex.). The example show the combination of socio-economic data and education data. 
```
data_combined = combine_sose_edu(sose_data, edu_data)
```
Both sose_data and edu_data have been ran through extract functions like in the example 1. The combine-function in this case merges the DataFrames using union over id and year. It also renames the columns.


## Functions
**extract_cancer(data, id_col=None, date_col=None, age_col=None, sex_col=None, diag_cols=None)**

Function for extracting data from cancer registry file **fcr_all_data.csv**. A pandas dataframe and wanted columns are given as an input. The function outputs a pandas dataframe with given columns. 

data = pandas dataframe loaded from **fcr_all_data.csv**

id_col = string containing name of id column. Required

date_col = string containing name of date column

age_col = string containing name of age column

sex_col = string containing name of sex column

diag_cols = list of strings containing names of diagnose columns 

**extract_birthday_sex(data, id_col=None, rel_col=None, sex_col=None, bdate_col =None, t_format='%Y%m%d')**

Function for extracting birthday and sex of the patient from files **thl2019_804_tljslv.sas7bdat** and **thl2019_804_tutkhenk.sas7bdat**. Can also interpret sex from parental relationships in file **thl2019_804_roolit.sas7bdat**. Outputs a pandas datframe containing either information on patients birthdate, sex or both.

data = pandas dataframe loaded from thl2019_804_tljslv.sas7bdat** or **thl2019_804_tutkhenk.sas7bdat**

id_col = string indicating name of id column

rel_col = string indicating name of relationship column. Used for interpreting sex.

sex_col = string indicating name of sex column

bdate_col = string indicating name of birthdate column

t_format = string indicating the format of the date in data. See https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior for more information about different choices. 
