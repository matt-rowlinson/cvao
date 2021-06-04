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
plt.rcParams['figure.figsize'] = (12, 4)
plt.style.use('seaborn-darkgrid')

colors=['#8dd3c7','#ffffb3','#bebada','#fb8072','#80b1d3','#fdb462','#b3de69',
        '#fccde5','#d9d9d9','#bc80bd','#ccebc5','#ffed6f']
colors=sns.color_palette("rocket",26)[5:]
styles=['dotted','dashed','dashdot','dotted','dashed','dashdot','dotted','dashed','dashdot','dotted','dashed','dashdot',
        'dotted','dashed','dashdot','dotted','dashed','dashdot','dotted','dashed','dashdot','dotted','dashed','dashdot']
markers=['.','v','*','<','x','>','P','h','D','s','|','d','^','+','p','X','8']

variables=['met']
for var in variables:
    df = rp.gaw_data(var)
    for col in df.columns:
        if 'qc' in col:
            continue
        x = df[df[col+'_qc'] < 999]
        plt.scatter(x.index, x[col])
        plt.savefig('plots/CV_met_%s.png' %col)
        plt.close()
    
    sys.exit()

    if var=='O3':
        df['2009-07-01' : '2009-09-30'] = np.nan
 
    try:
        df=df[df.flag != 999]
        df=df[df.flag != 999.99]
        df = df.drop('flag', 1)
    except:
        pass
    
    years = (df.resample('Y').mean()).index.year.astype(str)
    mean = df.mean()
    std = df.std()
    df = df.resample('MS').mean()
    monmean = df.groupby(df.index.month).mean()
    #xx = df['2010'].index.strftime('%b')
    
    for n,year in enumerate(years):
        if len(df[year]) == 12:
            x = df[year].index.strftime('%b')
            plt.plot(x, df[year][var], label=year, color=colors[n], linestyle=styles[n], marker=markers[n])
    
    plt.plot(x, monmean[var], color='darkgrey', linestyle='--', label='Period mean')
    plt.ylabel('%s, (%s)' %(d[var]['abbr'],d[var]['unit']))
    plt.legend(ncol=3)
    plt.savefig('plots/%s_seasonality.png' %var )
    plt.close()
