#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 14:24:25 2020

@author: mjr583
"""
import sys
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

## Get CVAO data from Merge file and put into DataFrame
df=CV.get_from_merge(d['O3'], timestep='D')
X,Y,time=CV.remove_nan_rows(df,df.index)
df=df['mean']
df=pd.DataFrame(df)
df.columns=['Value']
df['2009-07-01' : '2009-09-30'] = np.nan
cv=df
cv_dm=df.resample('D').mean()
cv_mm=df.resample('M').mean()

## Prepare data (remove nans) and get curve fit function
df = cv_mm
pref= 'cv'
dates = df.index ; start='2006' ; timestep="M"
XX=np.arange(len(df[df.columns[0]]))
idx=np.isfinite(df[df.columns[0]])
Y=df[df.columns[0]][idx]
X=XX[idx]
time=dates[idx]
z, p = np.polyfit(X, Y, 1)
output = CV.curve_fit_function_NAO(df, X, Y, start, timestep=timestep)
CV.plot_o3_curve_from_df(df,X, Y, output, timestep=timestep, pref=pref, savepath='/users/mjr583/cvao/plots/')

# Plot whole thing
plt.plot(df.index, df, linestyle='--', marker='o', color='#08519c', markeredgecolor='k',\
         markeredgewidth=0.5, label='Monthly means')
plt.plot(time, output[0], linestyle='-', color='#3182bd', label='First harmonic (seasonallity)')
plt.plot(time, output[1], linestyle='-', color='#6baed6', label='Quadratic polynomial fit')
plt.plot(time, X*output[2]+output[1][0], color='#bdd7e7', label='Linear trend ')

plt.legend()
plt.ylabel('$O_3$ (ppb)')
plt.savefig('plots/poly_function_output.png', dpi=200)
plt.close()


# Now plot decomposed components seperately
f, (ax1,ax2,ax3,ax4,ax5,ax6) = plt.subplots(6,1,figsize=(12,12))
ax=[ax1,ax2,ax3,ax4, ax5, ax6]

ax1.plot(df.index, df, linestyle='--', marker='o', color='b', markeredgecolor='k',\
         markeredgewidth=0.5, label='Monthly mean $O_3$ Cape Verde ')
ax1.set_ylabel('$O_3$ (ppb)')
ax1.legend()

ax2.plot(time, X*output[2]+output[1][0], color='b', label='Linear trendline')
ax3.plot(time, output[1], linestyle='-', color='b', label='Non-linear LSR of quadratic polynomial')
ax4.plot(time, output[0], linestyle='-', color='b', label='First harmonic (interannual seasonality)')
ax5.plot(time, output[0]-(X*output[2]), linestyle='-', color='b', label='Detrended seasonality')

#Get residual
Y= Y - output[-1][1]*X              # Remove linear trend component
Y = Y - output[-1][2]*X**2          # Remove non-linear trend component
Y = Y - ( output[0]-(X*output[2]) ) # Remove seasonal component
ax6.plot(time, Y, linestyle='-', color='b', label='Residual') # Plot residual

for axes in ax[1:-1]:
    axes.plot(df.index, df, linestyle='--', marker='o', color='lightgrey', markeredgecolor='k',\
         markeredgewidth=0.5, alpha=0.6)
    axes.set_ylabel('$O_3$ (ppb)')
    axes.legend()

ax1.set_ylabel('$O_3$ (ppb)')
ax1.legend()
ax6.legend()

plt.savefig('plots/seasonality-trend_breakdown.png', dpi=200)
plt.close()
