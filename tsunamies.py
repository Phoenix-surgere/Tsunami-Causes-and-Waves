# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 13:33:36 2019

@author: black

link to legend, because otherwise many codes are unusuable:
https://www.ngdc.noaa.gov/hazard/tsu_db.shtml

"""

import pandas as pd
import zipfile
import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt

zf = zipfile.ZipFile('seismic-waves.zip') 
waves = pd.read_csv(zf.open('waves.csv'))
sources = pd.read_csv(zf.open('sources.csv'))


waves['running_total'] = np.arange(1, len(waves)+1)  #to plot histogram of cumulative history
fig, (ax1, ax2) = plt.subplots(nrows=2)
sns.lineplot(ax=ax1, x='YEAR',y='running_total',data=waves)
sns.lineplot(ax=ax2, x='YEAR',y='running_total',data=waves)
ax2.set_xlim(1900, 2020 )
plt.show()

months = {
'January': 1.0, 'February': 2.0, 'March': 3.0, 'April': 4.0,
'May': 5.0, 'June': 6.0, 'July': 7.0, 'August': 8.0, 
'September': 9.0, 'October': 10.0, 'November': 11.0, 'December':12.0
          }
months = {v: k for k, v in months.items()}

waves.MONTH.replace(months,inplace=True)
by_month = pd.DataFrame(waves.MONTH.value_counts())
by_month = by_month.T

sns.barplot(data=by_month) 
plt.title('Tsunami volume by month')
plt.ylabel('Tsunamies')
plt.grid(True)
plt.xticks(rotation=90)
plt.show()
