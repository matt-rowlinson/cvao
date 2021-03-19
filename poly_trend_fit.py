#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 14:24:25 2020

@author: mjr583
"""
import sys
sys.path.append('/users/mjr583/python_lib')
import RowPy as rp
import CVAO_tools as CV
from CVAO_dict import CVAO_dict as d
import matplotlib.pyplot as plt
import pandas as pd
import netCDF4
import numpy as np
from sites_dicts import EPA_dict
plt.rcParams['figure.figsize'] = (12, 4)
gaw_path = '/users/mjr583/scratch/NCAS_CVAO/GAW_datasets/'
epa_path = '/users/mjr583/scratch/NCAS_CVAO/EPA_datasets/'

## CVAO
df=CV.get_from_merge(d['O3'], timestep='D')
X,Y,time=CV.remove_nan_rows(df,df.index)
df=df['mean']
df=pd.DataFrame(df)
df.columns=['Value']
df['2009-07-01' : '2009-09-30'] = np.nan
cv=df
cv_dm=df.resample('D').mean()
cv_mm=df.resample('M').mean()

## Mace Head
mh=pd.read_csv(gaw_path+'mc_ozone_2006_to_2018.csv', delimiter=',', index_col=0)
mh.index = pd.to_datetime(mh.index)
mh.columns=['Value']
mh_dm = mh.resample('D').mean()
mh_mm = mh.resample('M').mean()

## Getting trend curve
dfs = [cv_mm, mh_mm]
pref= ['cv','mh'] ; outputs=[] ; times=[]
for n, df in enumerate(dfs):
    dates = df.index ; start='2006' ; timestep="M"

    XX=np.arange(len(df[df.columns[0]]))
    idx=np.isfinite(df[df.columns[0]])
    Y=df[df.columns[0]][idx]

    X=XX[idx]
    time=dates[idx]
    
    z, p = np.polyfit(X, Y, 1)
    output = CV.curve_fit_function(df, X, Y, start, timestep=timestep)
   
    outputs.append(output) ; times.append(time)
    CV.plot_o3_curve_from_df(df,X, Y, output, timestep=timestep, pref=pref[n], savepath='/users/mjr583/cvao/plots/')
   
## Plot whole thing with trend lines
plt.plot(dfs[0].index, dfs[0], linestyle='--', marker='o', color='b', markeredgecolor='k',\
         markeredgewidth=0.5, label='Cape Verde ', alpha=0.6)
plt.plot(dfs[1].index, dfs[1], linestyle='--', marker='o', color='g', markeredgecolor='k',\
         markeredgewidth=0.5, label='Mace Head (Ire)', alpha=0.6)

plt.plot(times[0], outputs[0][1], linestyle='-', color='b')
plt.plot(times[1], outputs[1][1], linestyle='-', color='g')

plt.legend()
plt.ylabel('$O_3$ (ppb)')
plt.savefig('/users/mjr583/cvao/plots/ozone_trends.png', dpi=200)
plt.close()

print(df)
print(z)
