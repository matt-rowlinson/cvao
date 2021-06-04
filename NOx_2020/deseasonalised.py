# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 10:31:45 2019
Script to examine different deseasonalisation techniques. 
@author: ee11mr
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
plt.style.use('seaborn-darkgrid')
plt.rcParams['figure.figsize'] = (7, 7)
savepath  = 'plots/'

df=pd.read_csv('/mnt/lustre/users/mjr583/NCAS_CVAO/CVAO_datasets/NOx_Jan_2014-Dec_2020_with_flags_and_LOD_ppt.csv', index_col=0)
df=pd.DataFrame(df)
df.index=pd.to_datetime(df.index)
df['NO']=df['NO_pptV']
df['NO2']=df['NO2_pptV']

var='NO'
dff=df[df['%s_Flag' %var] < .200 ]
temp=dff[dff[var] >= 0. ]
temp = pd.DataFrame( temp[var] )
temp.columns = [var]
df=temp

hourly = df.resample('H').mean()
daily = df.resample('D').mean()
monthly = df.resample('M').mean()
yearly= df.resample('Y').mean()

years = np.arange(2006, 2006+len(yearly.index))
colors = ['#e5f5e0','#c7e9c0','R','#74c476','#41ab5d',\
              '#7fcdbb','#41b6c4','#1d91c0',\
              '#225ea8','b','#253494','#081d58','k']

## in test case just use Ozone data for now
data = df['NO'][:'2020']
years = len((data.resample('Y').mean()).index.year)

## method one - centered moving average
freq=12
rm_data = data.resample('M').mean()
ds1 = rm_data.rolling(window=freq,center=True).mean()

## method three - subtracting monthly average for each observation
mean = data.mean()
std = data.std()
monmean = data.groupby(data.index.month).mean()
deseas_factor = monmean / std
ds3=np.zeros(len(data))
for n,m in enumerate(data.index.month):
    ds3[n] = data[n] + (mean - monmean[m])
#print(len(ds3))
#print(hourly[:'2020'].dropna())
#print(monthly)
ds3 = pd.DataFrame(ds3[:])
ds3.index = pd.to_datetime(hourly[:'2020'].dropna().index,format='%d/%m/%Y')
ds3 = ds3.resample('M').mean()[0]

## method 4 - divide series by seasonal decomposition
from statsmodels.tsa.seasonal import seasonal_decompose
MODEL='multiplicative'
ds_data = data.resample('M').mean()
idx = np.isfinite(ds_data)
freq=12
result = seasonal_decompose(ds_data[idx], model=MODEL,freq=freq)

hold= [result.trend,result.seasonal,result.resid,result.observed, result.observed / result.seasonal]
ds4a = result.observed / result.seasonal
ds4 = ds4a.resample('M').mean()

## method five - 
a = ds_data / result.trend
iters = int(np.ceil(years / (14./3.)))
for iter in range(iters):
    idx= np.isfinite(a)
    result = seasonal_decompose(a[idx], model=MODEL, freq=freq)
    b = ds_data / result.seasonal
    idx = np.isfinite(b)
    result = seasonal_decompose(b[idx], model=MODEL, freq=freq)
    a = ds_data / result.trend
ds5 =  b.resample('M').mean()

labels = ['Observations','Moving average',\
          'Residuals of mean (monthly bins)','Normalised by seasonal decomposition',\
          'X-12 ARIMA method']
plt.rcParams['figure.figsize'] = (8, 8)
fig = plt.figure()
data_ = data.resample('M').mean()
ds = [data_, ds1,ds3,ds4,ds5]
for i in range(len(ds)):
    ax = fig.add_subplot(len(ds),1,i+1)
    x = data_.index[-len(ds[i]):]
    plt.plot(data_.index, data_, color='darkgrey',linestyle='--')
    ax.plot(x, ds[i])
    ax.set_title(labels[i])
    ax.set_ylabel('$O_3$ (ppbv)')

    plt.xlim(data.index[0], data.index[-1])
    #plt.ylim(13,44)
plt.tight_layout()
plt.savefig('plots/deseasonalisation_techniques.png')
plt.close()

plt.rcParams['figure.figsize'] = (12, 4)
plt.plot(data_, label='Observations',color='darkgrey',linestyle='--')
plt.plot(ds1, label='Moving average')
plt.plot(ds1.index[-len(ds3):], ds3, label='Residuals of mean')
plt.plot(ds4, label='Normalised by seasonal decomposition', linestyle='-.')
plt.plot(ds5, label='X-12 ARIMA method', linestyle='--')
plt.legend()
plt.ylabel('NO (pptv)')
plt.savefig('plots/deseasonalisation_comparison.png')
plt.close()

from scipy.stats.stats import pearsonr
data__ = ds3

y = np.array(data__)
xx = np.arange(len(y))
idx=np.isfinite(y)


z = np.polyfit(xx[idx],y[idx],1)
p = np.poly1d(z)
pcc, xxxx = pearsonr(xx[idx],y[idx])

print(str(np.round(z[0]*1e3,2)))
