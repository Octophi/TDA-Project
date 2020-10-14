#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 22:03:31 2020

@author: nathanl
"""

#import the necessary stuff
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from scipy.interpolate import InterpolatedUnivariateSpline
from ripser import ripser
from persim import plot_diagrams
import scipy.io.wavfile
from IPython.display import clear_output
from IPython.display import Audio


#load in song and display it as waveform
Fs, X = scipy.io.wavfile.read('journey.wav')
X = X/(2.0**15) #in as 16 bit shorts, convert to float
plt.figure()
plt.plot(np.arange(len(X))/float(Fs), X)
plt.xlabel("Time (secs)")
plt.title("Song Name")
plt.show()

#Audio('songname.wav')


#sliding window, assuming integer x, dim, Tau
def slidingWindowInt(x, dim, Tau, dT):
    N = len(x)
    numWindows = int(np.floor((N-dim*Tau)/dT)) #number of windows
    if numWindows <= 0:
        print("Error: Tau too large")
        return np.zeros((number_of_seconds_of_song, dim))
    X = np.zeros((numWindows, dim)) #2D array to store the windows
    idx = np.arange(N)
    for i in range(numWindows):
        #indices of the samples in window
        idxx = np.array(dT*i + Tau*np.arange(dim), dtype=np.int32)
        X[i, :] = x[idxx]
    return X



#dim*Tau here spans 1/2 second since Fs is the sample rate
dim = round(Fs/200)
Tau = 100
dT = Fs/100

Y = slidingWindowInt(X[0:Fs*3], dim, Tau, dT)

print("Y.shape = ", Y.shape)
#Mean-center and normalize
Y = Y - np.mean(Y, 1)[:, None]
Y = Y/np.sqrt(np.sum(Y**2, 1))[:, None]

PDs = ripser(Y, maxdim=1)['dgms']
pca = PCA()
Z = pca.fit_transform(Y)

#plot point cloud and persistence diagram for song
plt.figure(figsize=(8, 4))
plt.subplot(121)
plt.title("2D PCA")
plt.scatter(Z[:, 0], Z[:, 1])
plt.subplot(122)
plot_diagrams(PDs)
plt.title("Persistence Diagram")
plt.show()
    

    