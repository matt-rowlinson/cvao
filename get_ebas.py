#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 14:24:25 2020

@author: mjr583
"""
import sys
sys.path.append('/users/mjr583/python_lib/')
import CVAO_tools as CV
from CVAO_dict import CVAO_dict as d
import RowPy as rp
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (12, 4)
plt.style.use('seaborn-darkgrid')

variable='O3'
df = rp.gaw_data(variable)


plt.plot(df.flag)
plt.savefig('plots/ebas_flag_%s.png' %variable)
plt.close()

df = df[df.flag != 999.0]
df = df[df.flag != 999]
df = df[df.flag != .999]
mon = df.resample('M').mean()

Y = df['2007':][variable].resample('Y').mean() 
ax = Y.plot()
ax.set_ylabel('Annual mean $O_3$ (ppb)')
plt.savefig('plots/annual_mean.png')# %variable)
plt.close()

sys.exit()

plt.scatter(df.index, df[variable], alpha=.1)#, label='Ebas')
plt.plot(mon[variable], 'k-', label='Ebas data')
plt.ylabel(d[variable]['abbr']+' ('+d[variable]['unit']+')')
plt.legend()
plt.savefig('plots/ebas_%s_downloaded_30-4-21.png' %variable)
plt.close()
