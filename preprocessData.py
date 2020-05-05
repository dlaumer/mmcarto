#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 14:58:31 2020

@author: dlaumer
"""
import pandas as pd
import numpy as np
	
#Read file
df = pd.read_csv('Gender Inequality Index (GII).csv', delimiter=',')
# Delete all columns which are empty
df = df.dropna(axis='columns',how='all')
# Delete one specific column called Unnamed: 3
df = df.drop(columns = ['Unnamed: 3'])
# Replace all ".." with None
df = df.replace("..",np.NaN)
# Delete the last 19 rows because they contain data we don't need
df.drop(df.tail(19).index,inplace=True)
# Change the data type of the first column to float instead of string
df[list(df)[0]] = df[list(df)[0]].astype(float)
# Change the data type of the other columns to float instead of string
for i in range(2,len(list(df))):
    df[list(df)[i]] = df[list(df)[i]].astype(float)

# Change the name of the country to the one of the other file so that the joining works
df['Country'][df['Country']=='United States'] = 'United States of America'
df['Country'][df['Country']=='Congo (Democratic Republic of the)'] = 'Congo, Democratic Republic of the'
df['Country'][df['Country']=='Eswatini (Kingdom of)'] = 'Eswatini'
df['Country'][df['Country']=='Hong Kong, China (SAR)'] = 'Hong Kong'
df['Country'][df['Country']=='Korea (Republic of)'] ='Korea, Republic of'
df['Country'][df['Country']=='Moldova (Republic of)'] = 'Moldova, Republic of'
df['Country'][df['Country']=='Tanzania (United Republic of)'] = 'Tanzania, United Republic of'
df['Country'][df['Country']=='United Kingdom'] = 'United Kingdom of Great Britain and Northern Ireland'

# Sort the values by country for the join
df = df.sort_values(by=['Country'])

# Read in the second file with the 3 letter ids for the countries
df1 = pd.read_csv('countryIds.csv',delimiter=',')
# Only keep the two columns with the country name and the id
df1 = df1[['name','alpha-3']]
# Also sort for the join
df1 = df1.sort_values(by=['name'])
# Join the two datasets
df2 = pd.merge(df, df1, left_on='Country',right_on='name')

#Prepare the data for export to tsv
# Remove some unneeded columns
dfExport = df2.drop(columns = ["HDI Rank (2018)", "name"])
# Replace alll 0 values with None
df = df.replace(0,np.NaN)
# Rename the columns
dfExport = dfExport.rename({"alpha-3":"id", "Country":"name"}, axis='columns')
# Export to tsv
dfExport.to_csv("GII.tsv", index = False, sep = '	')

dfExportT = dfExport.transpose()
dfExportT = dfExportT.drop(['name'])
dfExportT = dfExportT.rename(index = {"id":"year"})
dfExportT.to_csv("GIIGraph.csv", sep = ',')

