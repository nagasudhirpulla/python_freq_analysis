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
from matplotlib import dates
from scipy.stats import norm
import datetime as dt
import math

'''
from argparse import ArgumentParser
# get the arguments from command line
parser = ArgumentParser()
parser.add_argument("-f", "--file", help="input file folder location", default='x')
args = parser.parse_args()
'''

# fall back input folder name
inputFolder = r'C:\Users\Nagasudhir\Documents\Python Projects\python_freq_analysis'
numBins = 100

# get the directory of the script file
# print(os.path.dirname(os.path.realpath(__file__)))
if('__file__' in globals()):
    inputFolder = os.path.dirname(os.path.realpath(__file__))

inputFilename = os.path.join(inputFolder, 'freq_input.xlsx')

# read the frequecy dataframe
freq_df = pd.read_excel(inputFilename)

# calculate the variance and mean of the dataframe
freq_mean, freq_std = norm.fit(freq_df.iloc[:, 1])

# plot the histogram of data with numBins
fig,ax = plt.subplots()
freq_df.hist(ax=ax,bins=numBins)

# plot the ideal normal distribution
freqSeries = np.linspace(freq_df.iloc[:, 1].min(), freq_df.iloc[:, 1].max(), numBins)
pdfSeries = norm.pdf(freqSeries, freq_mean, freq_std)
pdfFactor = freq_df.shape[0]/pdfSeries.sum()
ax.plot(freqSeries,pdfFactor*pdfSeries)

xRanges = ax.get_xlim()
yRanges = ax.get_ylim()

axisText = 'mean = %.3f Hz\n\nstandard=%.3f Hz\ndeviation'%(freq_mean, freq_std)

ax.text(xRanges[0] + 0.05*(xRanges[1]-xRanges[0]), yRanges[1]*0.75, axisText, style='italic',
        bbox={'facecolor':'#eeeeee', 'alpha':0.4, 'pad':10})

nowTimeStr = dt.datetime.now().strftime('%d_%m_%y_%H_%M_%S')
figFilename = os.path.join(inputFolder, 'output_%s.png'%(nowTimeStr))
plt.savefig(figFilename, bbox_inches='tight')

# find the number of times frequency change was more than 0.03 Hz
rgmoTimestamps = freq_df.copy()
rgmoTimestamps.iloc[0,1] = np.nan

for i in range(1,len(rgmoTimestamps)):
    if abs(freq_df.iloc[i,1] - freq_df.iloc[i-1,1]) < 0.03:
        rgmoTimestamps.iloc[i,1] = np.nan
    else:
        rgmoTimestamps.iloc[i,1] = 0
        
rgmoTimestamps.columns = ['time', 'rgmoReq']

# matplotlib date format object
hfmt = dates.DateFormatter('%H:%M')
fig, ax = plt.subplots()
ax.xaxis.set_major_formatter(hfmt)
plt.xticks(rotation=45)
ax.set_xlim(freq_df.iloc[0,0], freq_df.iloc[len(freq_df)-1,0])
ax.set_ylim(-0.001, 0.05)
ax.set_yticks([])
ax.plot(rgmoTimestamps['time'], rgmoTimestamps['rgmoReq'], 'x')
fig.suptitle('Events when frequency difference was greater than 0.03 Hz', size=10)
figFilename = os.path.join(inputFolder, 'rgmo_%s.png'%(nowTimeStr))
fig.savefig(figFilename, bbox_inches='tight')


with open('output.txt', 'w') as the_file:
    the_file.write('Number of times RGMO should have acted = {0}\n'.format(len(rgmoTimestamps[rgmoTimestamps['rgmoReq'] == 0])))
    the_file.write('Mean Frequency = %.3f Hz\n'%(freq_mean))
    the_file.write('Max Frequency = %.3f Hz\nMinimum Frequency = %.3f Hz\n'%(freq_df.iloc[:, 1].min(), freq_df.iloc[:, 1].max()))
    the_file.write('Standard Deviation = %.3f Hz\n'%(freq_std))
    the_file.write('Frequency Variation Index, FVI = %.3f\n'%(((freq_df.iloc[:, 1]-50).abs()**2).sum()*10/len(freq_df)))