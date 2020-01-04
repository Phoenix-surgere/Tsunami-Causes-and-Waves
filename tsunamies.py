# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 13:33:36 2019

@author: black
"""

import pandas as pd
import zipfile

zf = zipfile.ZipFile('seismic-waves.zip') 
waves = pd.read_csv(zf.open('waves.csv'))
sources = pd.read_csv(zf.open('sources.csv'))