# Documentation

## Extracting data
**Example 1.** Once you have loaded data from atlas, you can extract the wanted columns from that data. Lets use Socio-economic data as an example.
```
data = extract_sose(data, ['TNRO', 'vuosi', 'sose'])
```
This will extract the columns that are listed in the second input. The list is order specific. It will also do some preprocessing, such as remove rows with no yearly info and change NaN values to a number corresponding unknown value. The other extract function work similarly. 

##Combining DataFrames
**Example 2.** There are functions for combining DataFrames. These can be used to ultimately get a DataFrame that has information about the patients visits, such as [id, date, age, father_id, mother_id, sex, sose (socio-economic status), iscfi2013 (education orientation), kaste_t2(level of education), diagnoses]. (Note that sose will change into average income given visits year, socio-economic group and sex.). The example show the combination of socio-economic data and education data. 
```
data_combined = combine_sose_edu(sose_data, edu_data)
```
Both sose_data and edu_data have been ran through extract functions like in the example 1. The combine-function in this case merges the DataFrames using union over id and year. It also renames the columns.
