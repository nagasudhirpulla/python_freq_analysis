# -*- coding: utf-8 -*-
"""
Created on Sat Jun 30 19:45:21 2018

@author: Nagasudhir
https://stackoverflow.com/questions/10138085/python-pylab-plot-normal-distribution
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy.stats import norm

# fall back input folder name
inputFolder = r'C:\Users\Nagasudhir\Documents\Python Projects\python_freq_analysis'

# get the directory of the script file
# print(os.path.dirname(os.path.realpath(__file__)))
if('__file__' in globals()):
    inputFolder = os.path.dirname(os.path.realpath(__file__))

inputFilename = os.path.join(inputFolder, 'freq_input.xlsx')

# read the frequecy dataframe
freq_df = pd.read_excel(inputFilename)

# calculate the variance and mean of the dataframe
freq_mean, freq_std = norm.fit(freq_df.iloc[:, 1])

numBins = 100
fig,ax = plt.subplots()
freq_df.hist(ax=ax,bins=numBins)
freqLims = ax.get_xlim()

seriesRes = 1000
freqSeries = np.linspace(freqLims[0], freqLims[1], seriesRes)

#pdfFactor = freq_df.shape[0]*0.5/(freq_std * np.sqrt(2 * np.pi))
#ax.plot(freqSeries,pdfFactor*norm.pdf(freqSeries, freq_mean, freq_std))
    