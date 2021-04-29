#Log Analysis and Virtualization System
#Damien, Drake, and Becca
#Software Engineering Spring 2021
#4/26/2021
#Sprint 3

#===========================================================================================================================
#include dependencies for PyOD
from __future__ import division
from __future__ import print_function
import pandas as pd
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from pandas import DataFrame
import os
import sys
from time import time
import numpy as np
from numpy import percentile
import matplotlib.pyplot as plt
import matplotlib.font_manager
from pyod.models.cblof import CBLOF
import pyod.utils as ut
from sklearn import cluster

#read in normalized data from first script
normLogData = pd.read_csv (r'normalizedData.csv', header=None)
#print(normLogData)
stillThere = pd.read_csv (r'stillThere.csv', header=None)
#print(stillThere)
copyLogData = pd.read_csv(r'copyLogData.csv', header=None)

#Description: Applies PCA for dimensionality reduction. Only the sets of features that contribute the the variability of the
#data are kept. The others are discarded.  We use this to reduce runtime for user convenience.

#===========================================================================================================================

#Principal componenet analysis for dimensionality reduction
#referenced this tutorial -> https://www.datacamp.com/community/tutorials/principal-component-analysis-in-python
from sklearn.decomposition import PCA

#account for 90% variability of the data
pcaLog = PCA(0.90) 

#fit the model to data and reduce dimensionality (transform the data)
updatedData = pcaLog.fit_transform(normLogData) 

#hide main TK window
msg_wind = tk.Tk()
msg_wind.withdraw() 

#computes the number of principle components and shows user their number of principle components
messagebox.showinfo("Number of Principle Components to account for 90% of variability", pcaLog.n_components_)

#computes the percentage of variance accounted for per each principle component
varPerComp = pd.DataFrame(pcaLog.explained_variance_ratio_)
varPerComp = varPerComp.to_string()

#hide main TK window
m_win = tk.Tk()
m_win.withdraw() 

#show user the variance explained by each principle component
messagebox.showinfo("Variance explained by each principle component", varPerComp)

#===========================================================================================================================
#Description: Applies Cluster Based Local Outlier Factor, a popular anomaly detection algorithm.  We do this through utilizing
#the PyOD API/library.  Can be expanded upon in future use, by simply calling the methods for the other unsupervised anomaly 
#detection algorithms and following the format we have below.
#PyOD citation:
##Zhao, Y., Nasrullah, Z. and Li, Z., 2019. PyOD: A Python Toolbox for Scalable Outlier Detection. Journal of machine learning research (JMLR), 20(96), pp.1-7.

#===========================================================================================================================

#Referenced PyOD Creater's github to see how to use methods https://github.com/yzhao062/pyod/blob/master/notebooks/Compare%20All%20Models.ipynb******
#Referenced PyOD's documentation https://pyod.readthedocs.io/en/latest/pyod.html

#Create CBLOF Model with set contamination level. Future Work: User can set contamination level through GUI
#Uses all default settings: Kmeans is default for base clustering estimator (8 clusters)
clusBsdLocOutFact = CBLOF(contamination= 0.0385)

#Fit data to model
clusBsdLocOutFact.fit(updatedData)

#Generate CBLOF scores
cblofScores = (clusBsdLocOutFact.decision_function(updatedData) * -1)

#Predict if anomaly or not based on CBLOF score
anomalyScore = clusBsdLocOutFact.predict(updatedData)
anomalyScore = pd.DataFrame(anomalyScore)

#Only used for testing accuracy
anomalyScore.to_csv('anomalies_cblof.csv', index = False, header=False)

#===========================================================================================================================

#from pyod.models.lof import LOF
#from pyod.models.knn import KNN
#LOF
#locOutFact = LOF(n_neighbors=35, contamination=0.05)
#locOutFact.fit(updatedData)
#lofScores = locOutFact.decision_function(updatedData) * -1
#lofAnomScore = locOutFact.predict(updatedData)
#lofAnomScore = pd.DataFrame(lofAnomScore)
#lofAnomScore.to_csv('anomalies_lof.csv', index = False, header=False)

#===========================================================================================================================

#KNN - (K-Nearest Neighhbor)
#knnOutFact = KNN(contamination=0.05)
#knnOutFact.fit(updatedData)
#knnScores = knnOutFact.decision_function(updatedData) * -1
#knnAnomScore = knnOutFact.predict(updatedData)
#knnAnomScore = pd.DataFrame(knnAnomScore)
#knnAnomScore.to_csv('anomalies_knn.csv', index = False, header=False)

#Gets the number of anomalies detected and exports that as a CSV to be used for graphing.
finalAnomCounts = pd.DataFrame()

#Switches the columns order to facilitate graphing later: Limitation with JFreeCharts. Has no bearing on code other than making it look better.
finalAnomCounts = pd.DataFrame(anomalyScore[0].value_counts())
finalAnomCounts.insert(loc=1, column="New Column", value=[0, 1])
finalAnomCounts = finalAnomCounts.reindex([1,0])
columns_titles = ["New Column", 0]
finalAnomCounts = finalAnomCounts.reindex(columns=columns_titles)

finalAnomCounts.to_csv('finalAnomCounts.csv', index = False, header= False)
#===========================================================================================================================
#Description: Finds indices of the anomalies in the original data file for user convenience. 

#===========================================================================================================================
#Gets the locations of anomalies
anomaliesList = []

#Putting all anomalies (those with a score of 1) into a list
anomaliesList = anomalyScore.index[anomalyScore[0] == 1]

#Just for presentation purposes - will take out
anomaliesFrame = pd.DataFrame(anomaliesList)

#Creates empty list for the original indices to be stored
originalIndices = []

#References all the records that were not removed with timeframe selection (their positions in the original data)
still_there = stillThere.iloc[:,0].values.tolist()

#loops through anomalies (their updated position) and references still_there to find their original position in the input
for x in anomaliesList:
    if x < len(stillThere):
        originalIndices.append(still_there[x])

#Converts to dataframe in order to export as CSV
anomaliesDetectedFrame = copyLogData.iloc[originalIndices]
#anomaliesDetectedFrame
anomaliesDetectedFrame.to_csv('Anomalies.csv', index = False, header=False)

#Uses a similar method to getting the most common times to seperate out the time column for each anomaly and count the # to be used for graphing.
anomalyDatesList = []
anomalyDatesFrame = anomaliesDetectedFrame[41]
for i in anomalyDatesFrame.index:
        dateString = anomalyDatesFrame.loc[i]
        dateString = dateString[0:10]
        anomalyDatesList.append(dateString)
        
newAnomalyDatesFrame = pd.DataFrame(np.array([anomalyDatesList]).T)
newAnomalyDatesFrame.columns = [0]

finalDateCounts = pd.DataFrame()
finalDateCounts = newAnomalyDatesFrame[0].value_counts()

#finalDateCounts.sort_values(by=0)

finalDateCounts.to_csv('finalDateCounts.csv', index = True, header= False)


#Menu Stuff
user_update = tk.Tk()
user_update.withdraw() 
messagebox.showinfo("User Update", "Anomalies.csv has been created in your project directory.")