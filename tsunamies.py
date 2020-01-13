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
#waves = pd.read_csv(zf.open('waves.csv'))
sources = pd.read_csv(zf.open('sources.csv'))


sources['running_total'] = np.arange(1, len(sources)+1)  #to plot histogram of cumulative history

fig, (ax1, ax2) = plt.subplots(nrows=2)
sns.lineplot(ax=ax1, x='YEAR',y='running_total',data=sources)
sns.lineplot(ax=ax2, x='YEAR',y='running_total',data=sources)
ax2.set_xlim(1900, 2020 )
plt.show()

months = {
'January': 1.0, 'February': 2.0, 'March': 3.0, 'April': 4.0,
'May': 5.0, 'June': 6.0, 'July': 7.0, 'August': 8.0, 
'September': 9.0, 'October': 10.0, 'November': 11.0, 'December':12.0
          }
months = {v: k for k, v in months.items()}
sources.MONTH.replace(months,inplace=True)

valid = {-1.0 : 'Bad entry', 
         0.0: 'River-level effect',
         1.0: 'Very doubtful',
         2.0: 'Questionable',
         3.0: 'Probable',
         4.0: 'Definite'}
sources.VALIDITY.replace(valid,inplace=True)
sources.VALIDITY.value_counts().plot.pie()

by_month = pd.DataFrame(sources.MONTH.value_counts())
by_month = by_month.T

sns.barplot(data=by_month) 
plt.title('Tsunami volume by month')
plt.ylabel('Tsunamies')
plt.grid(True)
plt.xticks(rotation=90)
plt.show()

causes = {
0 : 'Unknown', 1 : 'Earthquake', 2 : 'Questionable Earthquake', 
3 : 'Earthquake and Landslide', 4 : 'Volcano and Earthquake', 
5 : 'Volcano, Earthquake, and Landslide', 6 : 'Volcano', 
7 : 'Volcano and Landslide', 8 : 'Landslide', 9 : 'Meteorological', 
10: 'Explosion', 11: 'Astronomical Tide', 
        }
sources.CAUSE.replace(causes,inplace=True)
by_cause = pd.DataFrame(sources.CAUSE.value_counts()).T
fig, (ax1,ax2) = plt.subplots(nrows=2, figsize=(7,7))
plt.xticks(rotation=90)

fig.suptitle('Tsunami Causes') # or plt.suptitle('Main title')
ax1.grid(True); ax2.grid(True)
ax1.title.set_text('Primary Causes')
ax2.title.set_text('Secondary Causes')
sns.barplot(ax=ax1, data=by_cause.iloc[:, 0:4], orient="h")
sns.barplot(ax=ax2, data=by_cause.iloc[:, 4:-1], orient="h")

by_country = pd.DataFrame(sources.COUNTRY.value_counts()).T
plt.xticks(rotation=90)
plt.title('Tsunamies per Country')
plt.grid(True)
sns.barplot(data=by_country.iloc[:, 0:15])

#Zooming in on height
fig, (ax1, ax2) = plt.subplots(nrows=2, figsize=(5,5))
sns.boxplot(y='MAXIMUM_HEIGHT', data=sources, ax=ax1)
sns.stripplot(y='MAXIMUM_HEIGHT', data=sources, ax=ax2)
ax1.set_ylim(0, 50)
plt.show()

height_bins = pd.cut(sources.MAXIMUM_HEIGHT, bins=3)
height_bins.dropna(inplace=True)
height_bins.reset_index(drop=True,inplace=True)
print('Wave Height equal binning: \n')
print(height_bins.value_counts())

#More comprehensive overview of intensities and magnitudes, together with height
fig, (ax1, ax2,ax3) = plt.subplots(nrows=3, figsize=(7,7))
fig.suptitle('Distplots of Intensity + Height')
sns.stripplot(y='MAXIMUM_HEIGHT', data=sources, ax=ax1)
sns.distplot(sources.MAGNITUDE_IIDA.dropna(), ax=ax2)
ax2.set_ylabel('MAGNITUDE_IIDA')
sns.violinplot(x=sources.INTENSITY_SOLOVIEV.dropna(), ax=ax3)
plt.show()

#Exploring the relationship between height and those metrics
sns.relplot(x='MAXIMUM_HEIGHT', y='INTENSITY_SOLOVIEV',data=sources, hue='VALIDITY')
sns.relplot(x='MAXIMUM_HEIGHT', y='MAGNITUDE_IIDA', data=sources,hue='VALIDITY')
plt.show()
plt.clf()

by_totals = {
0: '0', 1: '1-50', 2 : '51-100' , 3 : '101-1000',  4 : '>1001'}

by_dmg=  {   
0 : '0', 1 : '<1M', 2 : '1-5M', 3 : '5-25M', 4 : '>5M' }

sources.DAMAGE_TOTAL.replace(by_dmg, inplace=True)
totals = sources.filter(regex=r'.+_TOTAL').drop(columns=['DAMAGE_TOTAL'])
totals = totals.replace(by_totals)
sources[totals.columns] = totals

plt.title('Total Damage by Tsunamies and Sources')
plt.grid(True)
sns.countplot(x='DAMAGE_TOTAL', data=sources)

for col in sources[totals.columns]:
    plt.title(col)
    plt.grid(True)
    sns.countplot(x=col, data=sources)
    plt.show()

