#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import pandas as pd               # Pandas handles dataframes
import numpy as np
import scipy
import matplotlib                 # Numpy handles lots of basic maths operations
import matplotlib.pyplot as plt   # Matplotlib for plotting
import seaborn as sns             # Seaborn for beautiful plots
import statsmodels
import CVAO_tools as CV
from CVAO_dict import CVAO_dict as d
sys.path.append('/users/mjr583/python_lib/')
import RowPy as rp

variable='O3'
timestep='M'
alpha=.75 ; poly=2
Merge = True

if Merge == True:
    df=CV.get_from_merge(d[variable], timestep='H')
    X,Y,time=CV.remove_nan_rows(df,df.index)
    df=df['mean']
    df=pd.DataFrame(df)
    df.columns=['Value']
    print('Merge')
else:
    df = rp.gaw_data(variable)
    df = df[df.flag != 999.0]
    df=df[variable]
    df=pd.DataFrame(df)
    print('EBAS')

df['2009-07-01' : '2009-09-30'] = np.nan
df=df.resample(timestep).mean()
df.index.name = 'Xvalue'
df.columns = ['Yvalue']

df=pd.DataFrame({'Xvalue':np.arange(len(df.Yvalue)), 'Yvalue':df.Yvalue }, index=df.index )

idx=np.isfinite(df.Yvalue)
Yvalue=df.Yvalue[idx]
Xvalue=df.Xvalue[idx]
index=df.index[idx]
df=pd.DataFrame({'Xvalue':np.arange(len(Yvalue)), 'Yvalue':Yvalue }, index=index )

cv=df
monmean=cv.groupby(cv.index.month).mean()
anom = []
for n in range(len(cv.Yvalue)):
    nmonth=cv.index[n].month
    anom.append( cv.Yvalue[n] - monmean.Yvalue[nmonth] )

df = pd.DataFrame({'Xvalue':np.arange(len(Yvalue)),'Yvalue' : anom}, index=cv.index)


# Scatterplot
plt.scatter(df.index, df["Yvalue"], color="grey", marker="o", s=5)
plt.xlabel("X"), plt.ylabel("Y")
plt.title('(N = 100)')
plt.savefig('lowessplots/scatterplot.png')
plt.close()

# Create linear trend line
sns.regplot("Xvalue", "Yvalue", data=df,  color="grey", scatter_kws={"s": 10},
                     line_kws={"color":"r","alpha":1,"lw":1} ,fit_reg=True)
plt.xlabel("X"), plt.ylabel("Y")
plt.title('Test data - with linear trend line')
plt.savefig('lowessplots/linear_trendline.png')
plt.close()


def loc_eval(x, b):
    loc_est = 0
    for i in enumerate(b): loc_est+=i[1]*(x**i[0])
    return(loc_est)


def loess(xvals, yvals, data, alpha, poly_degree=1):
    all_data = sorted(zip(data[xvals].tolist(), data[yvals].tolist()), key=lambda x: x[0])
    xvals, yvals = zip(*all_data)
    evalDF = pd.DataFrame(columns=['v','g'])
    n = len(xvals)
    m = n + 1
    q = int(np.floor(n * alpha) if alpha <= 1.0 else n)
    avg_interval = ((max(xvals)-min(xvals))/len(xvals))
    v_lb = min(xvals)-(.5*avg_interval)
    v_ub = (max(xvals)+(.5*avg_interval))
    v = enumerate(np.linspace(start=v_lb, stop=v_ub, num=m), start=1)
    xcols = [np.ones_like(xvals)]
    for j in range(1, (poly_degree + 1)):
        xcols.append([i ** j for i in xvals])
    X = np.vstack(xcols).T

    for i in v:
        #print(i)
        iterpos = i[0]
        iterval = i[1]
        iterdists = sorted([(j, np.abs(j-iterval)) for j in xvals], key=lambda x: x[1])
        _, raw_dists = zip(*iterdists)
        scale_fact = raw_dists[q-1]
        scaled_dists = [(j[0],(j[1]/scale_fact)) for j in iterdists]
        weights = [(j[0],((1-np.abs(j[1]**3))**3 if j[1]<=1 else 0)) for j in scaled_dists]
        _, weights      = zip(*sorted(weights,     key=lambda x: x[0]))
        _, raw_dists    = zip(*sorted(iterdists,   key=lambda x: x[0]))
        _, scaled_dists = zip(*sorted(scaled_dists,key=lambda x: x[0]))
        W         = np.diag(weights)
        b         = np.linalg.inv(X.T @ W @ X) @ (X.T @ W @ yvals)
        local_est = loc_eval(iterval, b)
        iterDF2   = pd.DataFrame({
            'v'  :[iterval],
            'g'  :[local_est]
            })
        evalDF = pd.concat([evalDF, iterDF2])
    evalDF = evalDF[['v','g']]
    return(evalDF)

evalDF = loess("Xvalue", "Yvalue", data = df, alpha=alpha, poly_degree=poly)
print(len(evalDF['v']))

fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.scatter(df.index, df["Yvalue"], color="grey", marker="o", alpha=0.5,s=5, label="_nolegend_")
ax1.plot(df.index, evalDF['g'][1:], color='red', linewidth= 3, label="Test")
plt.title('LOWESS regression ( alpha = %s, polynomial degree = %s )' %(alpha, poly))


plt.xlabel(None), plt.ylabel("$O_3$ anomaly, ppb")
plt.legend()
plt.tight_layout()
plt.savefig('lowessplots/cv_%s%sm_lowess-a%s-p%s.png' %(variable, timestep, alpha, poly))
