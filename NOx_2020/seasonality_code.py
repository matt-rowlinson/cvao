# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 16:25:28 2021
Script for plotting annual monthly means to analyse seasonality over time
@author: Matthew Rowlinson
"""
import sys
sys.path.append('/users/mjr583/python_lib/')
import CVAO_tools as CV
from CVAO_dict import CVAO_dict as d
import RowPy as rp
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
plt.rcParams['figure.figsize'] = (12, 4)
plt.style.use('seaborn-darkgrid')

colors=['#8dd3c7','#ffffb3','#bebada','#fb8072','#80b1d3','#fdb462','#b3de69',
        '#fccde5','#d9d9d9','#bc80bd','#ccebc5','#ffed6f']
#colors=sns.color_palette("rocket",26)[5:]
styles=['dotted','dashed','dashdot','dotted','dashed','dashdot','dotted','dashed','dashdot','dotted','dashed','dashdot',
        'dotted','dashed','dashdot','dotted','dashed','dashdot','dotted','dashed','dashdot','dotted','dashed','dashdot']
markers=['.','v','*','<','x','>','P','h','D','s','|','d','^','+','p','X','8']

df=pd.read_csv('/mnt/lustre/users/mjr583/NCAS_CVAO/CVAO_datasets/NOx_Jan_2014-Dec_2020_with_flags_and_LOD_ppt.csv', index_col=0)
df=pd.DataFrame(df)
df.index=pd.to_datetime(df.index)
df['NO']=df['NO_pptV']
df['NO2']=df['NO2_pptV']

var='NO2'
df=df[df['%s_Flag' %var] < .200 ]
temp=df[df[var] >= 0. ]
temp = pd.DataFrame( temp[var] )
temp.columns = [var]
df=temp

years = (df.resample('Y').mean()).index.year.astype(str)
mean = df.mean()
std = df.std()
df = df.resample('MS').mean()
monmean = df.groupby(df.index.month).mean()

df = df.resample('MS').median()
monmean = df.groupby(df.index.month).median()


for n,year in enumerate(years):
    if len(df[year]) == 12:
        x = df[year].index.strftime('%b')
        plt.plot(x, df[year][var], label=year, color=colors[n], linestyle=styles[n], marker=markers[n])

plt.plot(x, monmean[var], color='darkgrey', linestyle='--', label='Period mean')
plt.ylabel('%s (%s)' %(d[var]['abbr'],d[var]['unit']))
plt.legend(ncol=3)
plt.savefig('plots/%s_seasonality.png' %var )
plt.close()
