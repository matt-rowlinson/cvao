#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 14:24:25 2020

@author: mjr583
"""
import sys
sys.path.append('/users/mjr583/scratch/python_lib')
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
df=CV.get_from_merge(d['O3'], timestep='H')
X,Y,time=CV.remove_nan_rows(df,df.index)
df=df['mean']
df=pd.DataFrame(df)
df.columns=['Value']
df['2009-07-01' : '2009-09-30'] = np.nan
cv_dm=df.resample('D').mean()
cv_mm=df.resample('M').mean()

## Mace Head
mh=pd.read_csv(gaw_path+'mc_ozone_2006_to_2018.csv', delimiter=',', index_col=0)
mh.index = pd.to_datetime(mh.index)
mh.columns=['Value']
mh_dm = mh.resample('D').mean()
mh_mm = mh.resample('M').mean()

## Bermuda
#be=pd.read_csv(gaw_path+'tud_ozone_2006_to_2019.csv', delimiter=',', index_col=0)
be=pd.read_csv(gaw_path+'EBAS_bmw_2006_to_2019.csv', delimiter=',', index_col=0)
be=pd.DataFrame(be['Value'])
print(be)

be.index = pd.to_datetime(be.index)
be_dm = be.resample('D').mean()
be_mm = be.resample('M').mean()

be2=pd.read_csv(gaw_path+'new_tud_ozone_2006_to_2020.csv', delimiter=',', index_col=0)
be2=be2[be2.Value != -999.0]
be2.index = pd.to_datetime(be2.index)
be_dm2 = be2.resample('D').mean()
be_mm2 = be2.resample('M').mean()

## Ragged Point
rag=pd.read_csv(gaw_path+'rag_ozone_2007_to_2016.csv', delimiter=',', index_col=0)
rag.index = pd.to_datetime(rag.index)
rag_dm = rag.resample('D').mean()
rag_mm = rag.resample('M').mean()

## Plot daily and monthly means for whole period
#plt.scatter(cv_dm.index, cv_dm, marker='o', color='b', s=1.5, alpha=0.3)
plt.scatter(be_dm.index, be_dm, marker='o', color='r', s=1.5, alpha=0.3)
#plt.scatter(mh_dm.index, mh_dm, marker='o', color='g', s=1.5, alpha=0.3)
plt.scatter(rag_dm.index, rag_dm, marker='o', color='y', s=1.5, alpha=0.3)


#plt.plot(cv_mm.index, cv_mm, linestyle='-', marker='o', color='b', markeredgecolor='k',\
#         markeredgewidth=0.5, label='Cape Verde ', alpha=0.8)
plt.plot(be_mm.index, be_mm, linestyle='-', marker='o', color='r', markeredgecolor='k',\
         markeredgewidth=0.5, label='Tudor Hill (Ber)', alpha=0.8)
#plt.plot(mh_mm.index, mh_mm, linestyle='-', marker='o', color='g', markeredgecolor='k',\
#         markeredgewidth=0.5, label='Mace Head (Ire)', alpha=0.8)
plt.plot(rag_mm.index, rag_mm, linestyle='-', marker='o', color='y', markeredgecolor='k',\
         markeredgewidth=0.5, label='Ragged Point (Bar)', alpha=0.8)
plt.legend()
plt.ylabel('$O_3$ (ppb)')
plt.savefig('/users/mjr583/scratch/NCAS_CVAO/plots/ragtudorhill_ozone_data.png', dpi=200)
plt.close()


## Plot daily and monthly means for whole period
plt.scatter(be_dm.index, be_dm, marker='o', color='r', s=1.5, alpha=0.3)
plt.scatter(be_dm2.index, be_dm2, marker='o', color='grey', s=1.5, alpha=0.3)


#         markeredgewidth=0.5, label='Cape Verde ', alpha=0.8)
plt.plot(be_mm.index, be_mm, linestyle='-', marker='o', color='r', markeredgecolor='k',\
         markeredgewidth=0.5, label='Tudor Hill (EBAS)', alpha=0.8)
plt.plot(be_mm2.index, be_mm2, linestyle='-', marker='o', color='grey', markeredgecolor='k',\
         markeredgewidth=0.5, label='Tudor Hill (NOAA)', alpha=0.8)
plt.legend()
plt.ylabel('$O_3$ (ppb)')
plt.savefig('/users/mjr583/scratch/NCAS_CVAO/plots/comp_bmw.png', dpi=200)
plt.close()


## Getting trend curve
dfs = [cv_mm, be_mm, mh_mm,rag_mm]
pref= ['cv','be','mh','rag'] ; outputs=[] ; times=[]
for n, df in enumerate(dfs):
    dates = df.index ; start='2006' ; timestep='M'

    XX=np.arange(len(df[df.columns[0]]))
    idx=np.isfinite(df[df.columns[0]])
    Y=df[df.columns[0]][idx]

    X=XX[idx]
    time=dates[idx]
    #times.append(time)
    print(n)
    print(len(Y), len(X), len(time))
    #X, Y, time = CV.remove_nan_rows(df['Value'], dates) 
    z, p = np.polyfit(X, Y, 1)
    output = CV.curve_fit_function(df, X, Y, start, timestep=timestep)
    #print(output[-1])
    outputs.append(output) ; times.append(time)
    CV.plot_o3_curve_from_df(df,X, Y, output, timestep=timestep, pref=pref[n], savepath='/users/mjr583/scratch/NCAS_CVAO/plots/')
   
## Plot whole thing with trend lines
#plt.plot(cv_mm.index, cv_mm, linestyle='--', marker='o', color='b', markeredgecolor='k',\
#         markeredgewidth=0.5, label='Cape Verde ', alpha=0.6)
plt.plot(be_mm.index, be_mm, linestyle='--', marker='o', color='r', markeredgecolor='k',\
         markeredgewidth=0.5, label='Tudor Hill (Ber)', alpha=0.6)
#plt.plot(mh_mm.index, mh_mm, linestyle='--', marker='o', color='g', markeredgecolor='k',\
#         markeredgewidth=0.5, label='Mace Head (Ire)', alpha=0.6)
plt.plot(rag_mm.index, rag_mm, linestyle='--', marker='o', color='y', markeredgecolor='k',\
         markeredgewidth=0.5, label='Ragged Point (Bar)', alpha=0.6)

#plt.plot(times[0], outputs[0][1], linestyle='-', color='b')
plt.plot(times[1], outputs[1][1], linestyle='-', color='r')
#plt.plot(times[2], outputs[2][1], linestyle='-', color='g')
plt.plot(times[3], outputs[3][1], linestyle='-', color='y')

plt.legend()
plt.ylabel('$O_3$ (ppb)')
plt.savefig('/users/mjr583/scratch/NCAS_CVAO/plots/ragtudorhill_ozone_trends.png', dpi=200)
plt.close()


dfs = [cv_mm, be_mm, mh_mm,rag_mm, be_mm2]
pref= ['cv','be','mh','rag', 'be2'] ; outputs=[] ; times=[]
for n, df in enumerate(dfs):
    dates = df.index ; start='2006' ; timestep='M'

    XX=np.arange(len(df[df.columns[0]]))
    idx=np.isfinite(df[df.columns[0]])
    Y=df[df.columns[0]][idx]

    X=XX[idx]
    time=dates[idx]
    #times.append(time)
    #X, Y, time = CV.remove_nan_rows(df['Value'], dates) 
    z, p = np.polyfit(X, Y, 1)
    output = CV.curve_fit_function(df, X, Y, start, timestep=timestep)
    #print(output[-1])
    outputs.append(output) ; times.append(time)
    CV.plot_o3_curve_from_df(df,X, Y, output, timestep=timestep, pref=pref[n], savepath='/users/mjr583/scratch/NCAS_CVAO/plots/')
   
## Plot whole thing with trend lines
plt.plot(be_mm.index, be_mm, linestyle='--', marker='o', color='r', markeredgecolor='k',\
         markeredgewidth=0.5, label='Tudor Hill (EBAS)', alpha=0.6)
plt.plot(be_mm2.index, be_mm2, linestyle='--', marker='o', color='grey', markeredgecolor='k',\
         markeredgewidth=0.5, label='Tudor Hill (NOAA)', alpha=0.6)

plt.plot(times[1], outputs[1][1], linestyle='-', color='r')
plt.plot(times[4], outputs[4][1], linestyle='-', color='grey')

plt.legend()
plt.ylabel('$O_3$ (ppb)')
plt.savefig('/users/mjr583/scratch/NCAS_CVAO/plots/two_tudorhill_ozone_trends.png', dpi=200)
plt.close()


## Plot WEST ATLANTIC daily and monthly means for whole period
## EPA site data
epas=[]
for i in EPA_dict:
    if EPA_dict[i]['use_site']:
        ef=pd.read_csv(epa_path+EPA_dict[i]['save_name']+'_ozone.csv',index_col=0)
        ef.index=pd.to_datetime(ef.index, format='%Y-%m-%d')
        epas.append(ef)
dor_dm=epas[0].resample('D').mean()
dor_mm=epas[0].resample('M').mean()
ind_dm=epas[1].resample('D').mean()
ind_mm=epas[1].resample('M').mean()
car_dm=epas[2].resample('D').mean()
car_mm=epas[2].resample('M').mean()

plt.scatter(be_dm.index, be_dm, marker='o', color='r', s=1.5, alpha=0.3)
plt.scatter(rag_dm.index, rag_dm, marker='o', color='y', s=1.5, alpha=0.3)
plt.scatter(dor_dm.index, dor_dm, marker='o', color='purple', s=1.5, alpha=0.3)
plt.scatter(ind_dm.index, ind_dm, marker='o', color='brown', s=1.5, alpha=0.3)
plt.scatter(car_dm.index, car_dm, marker='o', color='orange', s=1.5, alpha=0.3)

plt.plot(be_mm.index, be_mm, linestyle='-', marker='o', color='r', markeredgecolor='k',
        markeredgewidth=0.5, label='Tudor Hill (Ber)', alpha=0.8)
plt.plot(rag_mm.index, rag_mm, linestyle='-', marker='o', color='y', markeredgecolor='k',
        markeredgewidth=0.5, label='Ragged Point (Bar)', alpha=0.8)
plt.plot(dor_mm.index, dor_mm, linestyle='-', marker='o', color='purple', markeredgecolor='k',
        markeredgewidth=0.5, label='Dorchester (MD)', alpha=0.8)
plt.plot(ind_mm.index, ind_mm, linestyle='-', marker='o', color='brown', markeredgecolor='k',
        markeredgewidth=0.5, label='Indian River (FL)', alpha=0.8)
plt.plot(car_mm.index, car_mm, linestyle='-', marker='o', color='orange', markeredgecolor='k',
        markeredgewidth=0.5, label='Carteret (NC)', alpha=0.8)
plt.legend()
plt.ylabel('$O_3$ (ppb)')
plt.savefig('/users/mjr583/scratch/NCAS_CVAO/plots/west_atlantic_ozone_data.png', dpi=200)
plt.close()

## Getting trend curve
dfs = [be_mm,rag_mm,dor_mm,ind_mm,car_mm]
pref= ['be','rag','dor','ind','car'] ; outputs=[] ; times=[]
for n, df in enumerate(dfs):
    dates = df.index ; start='2006' ; timestep='M'

    XX=np.arange(len(df[df.columns[0]]))
    idx=np.isfinite(df[df.columns[0]])
    Y=df[df.columns[0]][idx]

    X=XX[idx]
    time=dates[idx]
    #times.append(time)
    #X, Y, time = CV.remove_nan_rows(df['Value'], dates) 
    z, p = np.polyfit(X, Y, 1)
    output = CV.curve_fit_function(df, X, Y, start, timestep=timestep)
    #print(output[-1])
    outputs.append(output) ; times.append(time)
    CV.plot_o3_curve_from_df(df,X, Y, output, timestep=timestep, pref=pref[n], savepath='/users/mjr583/scratch/NCAS_CVAO/plots/')
   
## Plot whole thing with trend lines
plt.plot(be_mm.index, be_mm, linestyle='-', marker='o', color='r', markeredgecolor='k',
         markeredgewidth=0.5, label='Tudor Hill (Ber)', alpha=0.8)
plt.plot(rag_mm.index, rag_mm, linestyle='-', marker='o', color='y', markeredgecolor='k',
         markeredgewidth=0.5, label='Ragged Point (Bar)', alpha=0.8)
plt.plot(dor_mm.index, dor_mm, linestyle='-', marker='o', color='purple', markeredgecolor='k',
         markeredgewidth=0.5, label='Dorchester (MD)', alpha=0.8)
plt.plot(ind_mm.index, ind_mm, linestyle='-', marker='o', color='brown', markeredgecolor='k',
         markeredgewidth=0.5, label='Indian River (FL)', alpha=0.8)
plt.plot(car_mm.index, car_mm, linestyle='-', marker='o', color='orange', markeredgecolor='k',
         markeredgewidth=0.5, label='Carteret (NC)', alpha=0.8)

plt.plot(times[0], outputs[0][1], linestyle='-', color='r')
plt.plot(times[1], outputs[1][1], linestyle='-', color='y')
plt.plot(times[2], outputs[2][1], linestyle='-', color='purple')
plt.plot(times[3], outputs[3][1], linestyle='-', color='brown')
plt.plot(times[4], outputs[4][1], linestyle='-', color='orange')

plt.legend()
plt.ylabel('$O_3$ (ppb)')
plt.savefig('/users/mjr583/scratch/NCAS_CVAO/plots/west_atlantic_ozone_trends.png', dpi=200)
plt.close()
