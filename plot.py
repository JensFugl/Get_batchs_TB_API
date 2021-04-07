# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 10:00:43 2021

@author: jensr
"""

import pandas as pd

import matplotlib.pyplot as plt

df = pd.read_pickle('data/lol.pkl')

ax = plt.subplots()

df['flowrate_avg'].plot()
df['ABV'].plot()
df['SG'].plot()