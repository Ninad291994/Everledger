#!/usr/bin/env python
# coding: utf-8

"""
Everledger Code Test
Author: Ninad G. Wadekar   
Date: 01/12/2021 
"""



# Import necessary libraries
import pandas as pd
import sys
import subprocess

pd.set_option("display.max_columns", None)

# Need xlrd library for reading data and formatting information from 
# excel files in the historical .xls format.
subprocess.check_call([sys.executable, '-m', 'pip', 'install',
'xlrd'])




""" Question 1 - Parse the attached employee__1_.xls file """

# Reading employee__1_.xls file and converting it to dataframe

df_employee = pd.read_excel('employee__1_.xls')
print('\n\nAnswer to Question 1:\n', df_employee)




""" Question 2 - Normalize the date fields into a standard format """

# Let's first check shape of dataframe, data type of each column in the
# dataframe and if there is null values in the dataframe

print('1. Shape of dataframe: ', df_employee.shape)
print('\n2. Datatype of each column in the dataframe:\n',\
       df_employee.dtypes)
print('\n3 .Number of null values in each column:\n',\
        df_employee.isna().sum())

# We can see from above column datatype description that Date of Birth and
# Date of Joining are object datatypes. Let's normalize these columns to 
# ISO date format YYYY-MM-DD.

# Normalizing Date of Birth column
df_employee['Date of Birth'] = pd.to_datetime(df_employee['Date of Birth'],\
                                errors='coerce')

# Normalizing Date of Joining column
df_employee['Date of Joining'] = pd.to_datetime(df_employee['Date of Joining'],\
                                errors='coerce')

print('\n\nAnswer to Question 2:\n')
print('Date of Birth and Date of Joining datatype changed:\n', df_employee.dtypes)
print('df_employee with normalized date column \n\n', df_employee)




""" Question 3 - Group the employee list based on the field Quarter of Joining and sorted 
by the field Date of Birth and print as dictionary {Q1 : [emp1, emp2, ...]}"""

# Since we need to groupby 'Quarter of Joining', let's first check unique values
# of this column. This will also make us aware if there is any incorrect value.
print('\nUnique values in Quarter of Joining column:\n',\
        df_employee['Quarter of Joining'].unique())

# Thus values in Quarter of Joining column are consistent and correct.

# Since we need to display employee name, let's check if there are
# more than one employees with same First Name.

print('\nResults show if First Name is same for multiple employees: \n',\
        df_employee['First Name'].value_counts())

# We can see from below results that some employees have same first
# names. To improve probability of uniquely identifing employee 
# belonging to particular Quarter in final results, we can merge  
# First Name and Last Name to create new column called Full Name.

df_employee['Full Name'] = df_employee[['First Name', 'Last Name']]\
                            .apply(lambda x: ' '.join(x), axis=1)

print('\n Dataframe with new column Full Name:\n',df_employee)

# Ref: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html
# Groupby preserves the order of rows of original dataframe within each group. 
# Thus we can sort first based on Date of Birth and then groupby Quarter of Joining 
# and subsequently converting results into dictionary

grouped_sorted_emp_dict = df_employee.sort_values(['Date of Birth'], ascending=False)\
                           .groupby('Quarter of Joining')['Full Name']\
                           .apply(list)\
                           .to_dict()
                           
print('\nResult:\n', grouped_sorted_emp_dict)


# Let's verify if above results are correct by comparing list of Q1 with
# list obtained by alternate method. 
# For verification, df_employee is filtered on rows with Quarter of Joining
# as Q1 and sliced to keep only First Name and Date of Birth columns. Further
# sliced dataframe is sorted in descending order of Date of Birth. This is
# alternate method which results into same sorted list of employees as above 
# based on Date of Birth and belonging to selected Quarter of Joining. 

verification_df = df_employee[df_employee['Quarter of Joining'] == 'Q1']\
                    [['Full Name', 'Date of Birth']]\
                    .sort_values('Date of Birth', ascending=False)

name_list_for_verification = list(verification_df['Full Name'])

# Let's check if list of Q1 in grouped_sorted_emp_dict is same as 
# name_list_for_verification
if name_list_for_verification == grouped_sorted_emp_dict['Q1']:
    print('\nLists are same.')
else:
    print('\nList are different.')

# Displaying dictionary in more readable format
print('\n\nAnswer to Question 3:\n')
for k, v in grouped_sorted_emp_dict.items():
    print(k, ':', v, '\n')
