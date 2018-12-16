# -*- coding: utf-8 -*-
"""
Created on Sat Jun 30 19:45:21 2018

@author: Nagasudhir
https://stackoverflow.com/questions/10138085/python-pylab-plot-normal-distribution

We are going to create a timeline with x axis as date and 
y axis as the scatter plot of the timestamps where the change in freq is greater than a threshold value
"""
import numpy as np

# find the number of times frequency change was more than 0.03 Hz
def GetRGMOTimestamps(freq_df, freq_diff_thresh = 0.03, time_col_index = 0, freq_col_index = 1):
    rgmoTimestamps = freq_df.copy()
    rgmoTimestamps.iloc[0,1] = np.nan
    
    for i in range(1,len(rgmoTimestamps)):
        if abs(freq_df.iloc[i,freq_col_index] - freq_df.iloc[i-1,freq_col_index]) < freq_diff_thresh:
            rgmoTimestamps.iloc[i,freq_col_index] = np.nan
        else:
            rgmoTimestamps.iloc[i,freq_col_index] = 0
            
    newCols = rgmoTimestamps.columns.tolist()
    newCols[time_col_index] = 'time'
    newCols[freq_col_index] = 'rgmoReq'
    rgmoTimestamps.columns = newCols
    
    # drop the column since it was used just to flag the timestamps
    rgmoTimestamps.drop(['rgmoReq'], axis=1)
    
    # drop all the nans
    rgmoTimestamps = rgmoTimestamps.dropna()
    
    return rgmoTimestamps
