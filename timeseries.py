#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#SBATCH --job-name=timeseries
#SBATCH --ntasks=1
#SBATCH --mem=100Mb
#SBATCH --partition=nodes
#SBATCH --time=00:10:00
#SBATCH --output=Logs/timeseries_%A.log
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib
matplotlib.use('agg')
sys.path.append('/users/mjr583/python_lib')
import GC_tools as GC
import RowPy as rp
from CVAO_dict import CVAO_dict as d
import CVAO_tools as CV
plt.style.use('seaborn-darkgrid')

variable='O3'
std=True    # Add standard deviation
tl=True     # Add linear trendline
ts='M'      # Select timestep

df=CV.get_from_merge(d[variable])
#df=df['2007':'2015']  # Use to change period
f,ax= plt.subplots(figsize=(12,4))
if std == False:
    df=df.resample(ts).mean()
    ax.plot(df.index, df.Value, 'k', label='CVAO')

elif std==True:
    mean=df.resample(ts).mean()
    df75=df.resample(ts).quantile(.75)
    df25=df.resample(ts).quantile(.25)
        
    ax.fill_between(mean.index, df25[df.columns[0]],df75[df.columns[0]],color='grey', alpha=.3)
    ax.plot(mean.index, mean, 'k', label='CVAO')

if tl:
    # calc the trendline
    XX=np.arange(len(df[df.columns[0]]))
    idx=np.isfinite(df[df.columns[0]])
    Y=df[df.columns[0]][idx]

    X=XX[idx]
    time=df.index[idx]

    z = np.polyfit(X, Y, 1)
    p = np.poly1d(z)
    ax.plot(df.index[idx],p(X),"r--")
    # print the line equation:
    print("y=%.6fx+(%.6f)"%(z[0],z[1]))

if std:
    plt.savefig('./plots/CV_timeseries_%s_std.png' %variable )
else:
    plt.savefig('./plots/CV_timeseries_v13_%s.png' %variable )
