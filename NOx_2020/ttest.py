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
no=temp

no=no.resample('W').mean()
mean = no.mean()
no = no-mean
f, ax = plt.subplots()
ax.plot(no, 'k-', label='CVAO NO anomaly')
ax.legend()
ax.set_ylabel('NO (pptv)' )
plt.savefig('plots/NO_anomaly.png')

var='NO2'
dff=df[df['%s_Flag' %var] < .200 ]
temp=dff[dff[var] >= 0. ]
temp = pd.DataFrame( temp[var] )
temp.columns = [var]
no2=temp

no2=no2.resample('W').mean()
mean = no2.mean()
no2 = no2-mean
f, ax = plt.subplots()
ax.plot(no2, 'k-', label='CVAO NO2 anomaly')
ax.legend()
ax.set_ylabel('NO2 anomaly (pptv)' )
plt.savefig('plots/NO2_anomaly.png')
