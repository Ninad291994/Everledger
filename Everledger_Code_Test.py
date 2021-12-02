#!/usr/bin/env python
# coding: utf-8

"""
Everledger Code Test
Author: Ninad G. Wadekar   
Date: 01/12/2021 
"""



# Importing necessary libraries
import pandas as pd
import sys
import subprocess
pd.set_option("display.max_columns", None)

# We need xlrd library for reading data and formatting information 
# from excel files in the historical .xls format.
subprocess.check_call([sys.executable, '-m', 'pip', 'install',\
'xlrd'])




""" Task 1 - Parse the attached employee__1_.xls file """

# Reading employee__1_.xls file and parsing it to dataframe
df_employee = pd.read_excel('employee__1_.xls')
print('\n\nAnswer to Task 1:\n', df_employee)




""" Task 2 - Normalize the date fields into a standard format """

# 1. Check 1
# Let's first check shape of dataframe, data type of each column in the
# dataframe and if there are null values in the dataframe
print('1. Shape of dataframe: ', df_employee.shape)
print('\n2. Datatype of each column in the dataframe:\n',\
       df_employee.dtypes)
print('\n3 .Number of null values in each column:\n',\
        df_employee.isna().sum())

# 2. Normalization of Date of Joining
# We can see from above column datatype description that Date of 
# Joining are object datatypes. Let's normalize these columns to 
# standard date format yyyy-mm-dd.

df_employee['Date of Joining'] = pd.to_datetime(df_employee['Date of Joining'],\
                                              errors='coerce')

# Let's check if quarter of joining is correct according to date
# of joining
print('\n\nIncorrect Quarters as per date of joining:\n')
for i in range(len(df_employee)):
    m = df_employee['Date of Joining'].iloc[i].month
    q = ((m-1)//3)+1
    quarter = 'Q'+str(q)
    if quarter != df_employee['Quarter of Joining'].iloc[i]:
        print(df_employee.iloc[[i]])
        print('\n\n')
        
# We can see from below results that there are some rows with quarter
# of joining not consistent with date of joining. After investigating
# it seems like these rows had date in yyyy-mm-dd HH:MM:SS format in
# original dataframe.

# Assumption: I am assuming for these rows that quarters are incorrect
# and changed the quarters to correct ones. 
for i in range(len(df_employee)):
    m = df_employee['Date of Joining'].iloc[i].month
    q = ((m-1)//3)+1
    quarter = 'Q'+str(q)
    if quarter != df_employee['Quarter of Joining'].iloc[i]:
        df_employee.iloc[i, df_employee.columns.\
                         get_loc("Quarter of Joining")] = quarter
        


# However, if we assume that quarters were correct for these rows but 
# in date of joining places of month and day were mistakenly replaced,
# we will have to modify dates. There is no way to assume that


# 3. Normalization of Date of Birth column
df_employee['Date of Birth'] = pd.to_datetime(df_employee['Date of Birth'],\
                                              errors='coerce')

print('\n\nAnswer to Task 2:\n')
print('Date of Birth and Date of Joining datatype changed:\n', df_employee.dtypes)
print('\n\ndf_employee with normalized date column \n\n', df_employee)




""" Task 3 - Group the employee list based on the field Quarter of Joining and sorted 
by the field Date of Birth and print as dictionary {Q1 : [emp1, emp2, ...]}"""


# 1. Check 1
# Since we need to groupby 'Quarter of Joining', let's first check unique values
# of this column. This will also make us aware if there are any incorrect values.
print('\nUnique values in Quarter of Joining column:\n',\
        df_employee['Quarter of Joining'].unique())

# Thus, values in Quarter of Joining column are consistent and correct.


# 2. Check 2
# Since we need to display employee name, let's check if there are
# more than one employees with same First Name.
print('\nResults show if First Name is same for multiple employees: \n',\
        df_employee['First Name'].value_counts())

# We can see from above results that some employees have same first
# names. To improve probability of uniquely identifing employees 
# belonging to particular Quarter in final results, we can merge  
# First Name and Last Name to create new column called Full Name.

df_employee['Full Name'] = df_employee[['First Name', 'Last Name']]\
                            .apply(lambda x: ' '.join(x), axis=1)

print('\n Dataframe with new column Full Name:\n',df_employee)


# 3. Sorting and Grouping
# Ref: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html
# Groupby preserves the order of rows of original dataframe within each group. 
# Thus we can sort first based on Date of Birth and then groupby Quarter of Joining 
# and subsequently converting results into dictionary

grouped_sorted_emp_dict = df_employee.sort_values(['Date of Birth'], ascending=False)\
                           .groupby('Quarter of Joining')['Full Name']\
                           .apply(list)\
                           .to_dict()
                           
print('\nResult:\n', grouped_sorted_emp_dict)


# 4. Verification of results by alternate method
# Let's verify if above results are correct by comparing list of Q1 with
# list obtained by alternate method. For verification, df_employee is 
# filtered on rows with Quarter of Joining as Q1 and sliced to keep only 
# First Name and Date of Birth columns. Further sliced dataframe is sorted 
# in descending order of Date of Birth. This is alternate method which 
# results into same sorted list of employees as above  based on Date of 
# Birth and belonging to selected Quarter of Joining. 
verification_df = df_employee[df_employee['Quarter of Joining'] == 'Q1']\
                    [['Full Name', 'Date of Birth']]\
                    .sort_values('Date of Birth', ascending=False)

name_list_for_verification = list(verification_df['Full Name'])

# Let's check if list of Q1 in grouped_sorted_emp_dict is same as 
# name_list_for_verification
if name_list_for_verification == grouped_sorted_emp_dict['Q1']:
    print('\nLists are same. Hence, results are correct and verified.')
else:
    print('\nList are different. Results might be incorrect.')


# 5. Displaying results
# Displaying dictionary in more readable format
print('\n\nAnswer to Task 3:\n')
for k, v in grouped_sorted_emp_dict.items():
    print(k, ':', v, '\n')
