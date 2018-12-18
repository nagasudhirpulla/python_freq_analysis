# -*- coding: utf-8 -*-
"""
Created on Sat Jun 30 19:45:21 2018

@author: Nagasudhir
https://stackoverflow.com/questions/10138085/python-pylab-plot-normal-distribution

We are going to create a timeline with x axis as date and 
y axis as the scatter plot of the timestamps where the change in freq is greater than a threshold value
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import glob
from rgmo_detector import GetRGMOTimestamps

'''
from argparse import ArgumentParser
# get the arguments from command line
parser = ArgumentParser()
parser.add_argument("-f", "--file", help="input file folder location", default='x')
args = parser.parse_args()
'''

# fall back input folder name
inputFolder = r'C:\Users\Nagasudhir\Documents\Python Projects\python_freq_analysis'

# configuration settings
freq_col_index = 1
time_col_index = 0
freq_diff_thresh = 0.03

# get the directory of the script file
if('__file__' in globals()):
    inputFolder = os.path.dirname(os.path.realpath(__file__))
    # print(inputFolder)

dataFilesList = glob.glob(inputFolder + '/*.xlsx')

# inputFilename = os.path.join(inputFolder, 'freq_input.xlsx')

# initialize the main dataframe
rgmoTimestamps = pd.DataFrame(columns = ['time'])

for fileIter, inputFilename in enumerate(dataFilesList):
    # read the frequecy dataframe
    freq_df = pd.read_excel(inputFilename)
    # get the rgmoTimestamps of this iteration
    rgmoTimestampsChunk = GetRGMOTimestamps(freq_df, freq_diff_thresh, time_col_index, freq_col_index)
    # append this to the main dataframe
    rgmoTimestamps = pd.concat([rgmoTimestamps, rgmoTimestampsChunk], ignore_index=True)

# split the date and time of the column 'time'
rgmoTimestamps['time_of_day'] = rgmoTimestamps['time'].apply(lambda x: x.time())
rgmoTimestamps['date'] = rgmoTimestamps['time'].apply(lambda x: x.date())

plt.scatter(x=rgmoTimestamps.date.values, y=rgmoTimestamps.time_of_day.values)

# nowTimeStr = dt.datetime.now().strftime('%d_%m_%y_%H_%M_%S')
'''
writer = pd.ExcelWriter('output.xlsx')
rgmoTimestamps.to_excel(writer,'Sheet1')
writer.save()
'''