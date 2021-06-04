#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 14:24:25 2020

@author: mjr583
"""
import sys
sys.path.append('/users/mjr583/python_lib')
import CVAO_tools as CV
import RowPy as rp
from CVAO_dict import CVAO_dict as d
import matplotlib.pyplot as plt
import pandas as pd
import netCDF4
import numpy as np
from sites_dicts import EPA_dict
from scipy.optimize import curve_fit
from sklearn.metrics import mean_squared_error, r2_score
plt.rcParams['figure.figsize'] = (12, 4)
plt.style.use('seaborn-darkgrid')

df=pd.read_csv('/mnt/lustre/users/mjr583/NCAS_CVAO/CVAO_datasets/NOx_Jan_2014-Dec_2020_with_flags_and_LOD_ppt.csv', index_col=0)
df=pd.DataFrame(df)
df.index=pd.to_datetime(df.index)
df['NO']=df['NO_pptV']
df['NO2']=df['NO2_pptV']
#print(df)

var='NO'
dff=df[df['%s_Flag' %var] < .200 ]
temp=dff[dff[var] >= 0. ]
temp = pd.DataFrame( temp[var] )
temp.columns = [var]
dff=temp

dff = dff.resample('D').median()
f, ax = plt.subplots()
ax.scatter(dff.index, dff['NO'], alpha=.1)
ax.plot(dff.NO.resample('M').mean(), 'k-', label='CVAO NO')
ax.legend()
ax.set_ylabel('NO (pptv)' )
ax.set_yscale('log')
plt.savefig('plots/CV_NO.png')


var='NO2'
dff=df[df['%s_Flag' %var] < .200 ]
temp=dff[dff[var] >= 0. ]
temp = pd.DataFrame( temp[var] )
temp.columns = [var]
dff=temp


dff = dff.resample('D').median()
f, ax = plt.subplots()
ax.scatter(dff.index, dff['NO2'], alpha=.1)
ax.plot(dff.NO2.resample('M').mean(), 'k-', label='CVAO NO2')
ax.legend()
ax.set_ylabel('NO2 (pptv)' )
ax.set_yscale('log')
plt.savefig('plots/CV_NO2.png')
plt.close()


no = df[df['NO_Flag'] < .200]
no_years = no.index.year.drop_duplicates().tolist()
no_=[]
for year in no_years[:-1]:
    print(year, no['NO'][str(year)].count(), np.round(no['NO'][str(year)].mean(),2))
    no_.append( no['NO'][str(year)].mean() )

no2 = df[df['NO2_Flag'] < .200]
no2_years = no2.index.year.drop_duplicates().tolist()
no2_=[]
for year in no2_years[:-1]:
    print(year, no2['NO2'][str(year)].count(), np.round(no2['NO2'][str(year)].mean(),2))
    no2_.append( no2['NO2'][str(year)].mean() )

f, ax = plt.subplots()
#ax2=ax.twinx()
ax.plot( no_years[:-1], no_ , label='NO', color='b')
#ax2.plot( no2_years[:-1], no2_ , label='NO2', color='g')
#ax.set_yscale('log')
ax.set_ylabel('NO (ppt)')
ax.legend(loc=2)
#ax2.legend(loc=1)
plt.savefig('plots/annual_means_NOx.png')
plt.close()


