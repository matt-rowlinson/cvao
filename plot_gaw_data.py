#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 14:24:25 2020

@author: mjr583
"""
import sys
sys.path.append('/users/mjr583/python_lib/')
import CVAO_tools as CV
import RowPy as rp
import matplotlib.pyplot as plt
import pandas as pd
import netCDF4
import numpy as np
plt.rcParams['figure.figsize'] = (12, 4)

df = rp.gaw_data('O3')
plt.plot(df["var"])
plt.savefig('./tester.png')

## Mace Head
gaw_path='/users/mjr583/scratch/NCAS_CVAO/GAW_datasets/'
mh=pd.read_csv(gaw_path+'mc_ozone_2006_to_2018.csv', delimiter=',', index_col=0)
mh.index = pd.to_datetime(mh.index)
mh.columns=['Value']
mh_dm = mh.resample('D').mean()
mh_mm = mh.resample('M').mean()

## Bermuda
be=pd.read_csv(gaw_path+'ber_ozone_2006_to_2018.csv', delimiter=',', index_col=0)
be.index = pd.to_datetime(be.index)
be_dm = be.resample('D').mean()
be_mm = be.resample('M').mean()

## Plot daily and monthly means for whole period
plt.scatter(cv_dm.index, cv_dm, marker='o', color='b', s=1.5, alpha=0.3)
plt.scatter(be_dm.index, be_dm, marker='o', color='r', s=1.5, alpha=0.3)
plt.scatter(mh_dm.index, mh_dm, marker='o', color='g', s=1.5, alpha=0.3)

plt.plot(cv_mm.index, cv_mm, linestyle='-', marker='o', color='b', markeredgecolor='k',\
         markeredgewidth=0.5, label='Cape Verde ', alpha=0.8)
plt.plot(be_mm.index, be_mm, linestyle='-', marker='o', color='r', markeredgecolor='k',\
         markeredgewidth=0.5, label='Tudor Hill (Ber)', alpha=0.8)
plt.plot(mh_mm.index, mh_mm, linestyle='-', marker='o', color='g', markeredgecolor='k',\
         markeredgewidth=0.5, label='Mace Head (Ire)', alpha=0.8)

plt.legend()
plt.ylabel('$O_3$ (ppb)')
plt.savefig('/users/mjr583/scratch/NCAS_CVAO/plots/atlantic_o3_data.png', dpi=200)
plt.close()

## Getting trend curve
dfs = [cv_mm, be_mm, mh_mm]

pref= ['cv','be','mh'] ; outputs=[] ; times=[]
for n, df in enumerate(dfs):
    
    dates = df.index ; start='2006' ; timestep='M'
    X, Y, time = CV.remove_nan_rows(df['Value'], dates)  
    z, p = np.polyfit(X, Y, 1)
    print(z*12)
    output = CV.curve_fit_function(df, X, Y, start, timestep=timestep)
    outputs.append(output) ; times.append(time)
    CV.plot_o3_curve_from_df(df,X, Y, output, timestep=timestep, pref=pref[n], savepath='/users/mjr583/scratch/NCAS_CVAO/plots/')
   
## Plot whole thing with trend lines
plt.plot(cv_mm.index, cv_mm, linestyle='--', marker='o', color='b', markeredgecolor='k',\
         markeredgewidth=0.5, label='Cape Verde ', alpha=0.6)
plt.plot(be_mm.index, be_mm, linestyle='--', marker='o', color='r', markeredgecolor='k',\
         markeredgewidth=0.5, label='Tudor Hill (Ber)', alpha=0.6)
plt.plot(mh_mm.index, mh_mm, linestyle='--', marker='o', color='g', markeredgecolor='k',\
         markeredgewidth=0.5, label='Mace Head (Ire)', alpha=0.6)
    
plt.plot(times[0], outputs[0][1], linestyle='-', color='b')
plt.plot(times[1], outputs[1][1], linestyle='-', color='r')
plt.plot(times[2], outputs[2][1], linestyle='-', color='g')

plt.legend()
plt.ylabel('$O_3$ (ppb)')
plt.savefig('/users/mjr583/scratch/NCAS_CVAO/plots/atlantic_o3_data_trend.png', dpi=200)
plt.close()


## Plot CV ozone with uncertainty
file='/users/mjr583/scratch/NCAS_CVAO/CVAO_datasets/precision.csv'
err = pd.read_csv(file,index_col=0)
err.index = pd.to_datetime(cv_mm.index)
err.columns = ['Precision']
err.fillna(0,inplace=True)

plt.fill_between(cv_mm.index, cv_mm.Value - err.Precision, cv_mm.Value + err.Precision, color='grey')
plt.plot(cv_mm.index, cv_mm, linestyle='-', marker='o', color='b', linewidth=1, markeredgecolor='k',\
         markeredgewidth=0.5, label='Cape Verde ')
    
plt.plot(times[0], outputs[0][1], linestyle='-', color='k')
plt.ylabel('$O_3$ (ppb)')
plt.savefig('/users/mjr583/scratch/NCAS_CVAO/plots/cvao_o3_precision.png', dpi=200)
plt.show()

