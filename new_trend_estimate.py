#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 14:24:25 2020

@author: mjr583
"""
import sys
import CVAO_tools as CV
sys.path.append('/users/mjr583/python_lib')
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
variable='O3'
averaging='mean'
year=False


## Get CVAO data from Merge file and put into DataFrame
#df=CV.get_from_merge(d[species])#, timestep='D')
#X,Y,time=CV.remove_nan_rows(df,df.index)
#df=df[averaging]
#df=pd.DataFrame(df)
if variable=='NOx':
    df=pd.read_csv('/mnt/lustre/users/mjr583/NCAS_CVAO/CVAO_datasets/NOx_Jan_2014-Dec_2020_with_flags_and_LOD_ppt.csv', index_col=0)
    df=pd.DataFrame(df)
    df.index=pd.to_datetime(df.index)
    df[variable]=df['NO_pptV']+df['NO2_pptV']
    print(df) 
    df=pd.DataFrame(df)
    df.index=pd.to_datetime(df.index)
    df[variable]=df['NO_pptV']+df['NO2_pptV']
    print(df)
else:
    df = rp.gaw_data(variable)
df=df[variable]
df=pd.DataFrame(df)
df.columns=['Value']
#print(df)
years=df.index.year.drop_duplicates().tolist()
for year in years:
    pass
    #print(df[str(year)].mean())

df=df['2015':'2019']
plt.scatter(df.index, df['Value'], alpha=.1)#label='20200908_CV_Merge')
plt.plot(df.Value.resample('M').mean(), 'k-', label='CVAO %s' %variable)
plt.legend()
plt.ylabel('%s (ppbv)' %variable)
plt.savefig('plots/Merge_20200908_CV_%s.png' %variable)
#sys.exit()

df.columns=['Value']
if variable == 'O3':
    df['2009-07-01' : '2009-09-30'] = np.nan
if year:
    df=df[year:]
cv=df
cv_dm=df.resample('D').mean()
cv_mm=df.resample('M').mean()


cv=cv_mm
monmean=cv.groupby(cv.index.month).mean()
anom = []
for n in range(len(cv.Value)):
    nmonth=cv.index[n].month
    anom.append( cv.Value[n] - monmean.Value[nmonth] )

df = pd.DataFrame({'anomaly' : anom}, index=cv.index)

df.plot()
plt.savefig('plots/anomaly_scatterplot.png')
plt.close()


#df = cv_mm
pref= 'Cooper_cv'
dates = df.index ; start='2006' ; timestep="M"
XX=np.arange(len(df[df.columns[0]]))
idx=np.isfinite(df[df.columns[0]])
Y=df[df.columns[0]][idx]
X=XX[idx]
time=dates[idx]
z, p = np.polyfit(X, Y, 1)

df=df[idx]
output = CV.linear_regression_model(df, X, Y, start, timestep=timestep)

CV.plot_o3_curve_from_df(df,X, Y, output, timestep=timestep, pref=pref, savepath='/users/mjr583/cvao/new_plots/')

# Plot whole thing
f,ax = plt.subplots(figsize=(12,4))
ax.plot(df.index, df, linestyle='--', marker='o', color='#08519c', markeredgecolor='k',\
         markeredgewidth=0.5, label='Monthly means')
ax.plot(time, output[0], linestyle='-', color='#3182bd', label='First harmonic (seasonallity)')
ax.plot(time, output[1], linestyle='-', color='#6baed6', label='Quadratic polynomial fit')
ax.plot(time, X*output[2]+output[1][0], linestyle='--', color='#bdd7e7', label='Linear trend ')

plt.legend()
plt.ylabel('$NO_x$ (ppt)')
ax.set_yscale('log')
plt.savefig('new_plots/linear_regression_function_output.png', dpi=200)
plt.close()

trend_per_year=np.round(output[-1][1]*12,2)
trend_per_decade=np.round(output[-1][1]*12*10, 2)
print('O3 trend per year = %s ppb yr-1' %trend_per_year)
print('O3 trend per decade = %s ppb decade-1' %trend_per_decade)
