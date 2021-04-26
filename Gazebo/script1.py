#Log Analysis and Virtualization System
#Damien, Drake, and Becca
#Software Engineering Spring 2021
#4/13/2021
#Sprint 2

#===========================================================================================================================

#Description: User is prompted to select a log data CSV file.  It is turned into a dataframe.

#include dependencies
import numpy as np
import pandas as pd
import re as re
from sklearn import preprocessing
from sklearn.preprocessing import LabelEncoder
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from pandas import DataFrame

#creates a menu for file selection
#https://www.w3schools.in/python-tutorial/gui-programming/
#https://www.tutorialspoint.com/askopenfile-function-in-python-tkinter#:~:text=Python%20Server%20Side%20Programming%20Programming%20Instead%20of%20hard,a%20button%20on%20it%20to%20browse%20the%20files.
file_menu = Tk()
file_menu.geometry('700x300')
file_menu.title("Data File Selection: Select one data file please. Close window once you have made your selection.")

#gains access to the user's file system
#===========================================================================================================================
def open_file():
    global user_input
    user_input = filedialog.askopenfile(filetypes=[('CSV Files','.csv')],initialdir="/", mode="r",multiple=False)
#===========================================================================================================================    

#restricts user access to only CSVs, triggers menu when user clicks the button
user_button = Button(file_menu, text = 'Click here to view file options: CSV files only', command = lambda:open_file())
user_button.pack()
user_button.mainloop()

#Getting a sample of records to determine which column holds the timestamp
#the first 5 rows should tell us which column has the dates, it would be rare to have no timestamps in any of the 5 rows
try: 
    logData = pd.read_csv(user_input, header=None)
    sample = logData.head()
except:
    error_window = tk.Tk()
    error_window.withdraw() 
    messagebox.showinfo("Error", "Window closed without selection, or other error occured.")

#===========================================================================================================================
#Description: Locates the busiest times in the network to display to user. 

#===========================================================================================================================

#Copies logData for later use in index matching
copyLogData = logData.copy(deep = True)
copyLogData.to_csv('copyLogData.csv', index = False, header = False)

#Creates a list to hold just the dates column
datesList = []

#Looks for most common times on the network
#===========================================================================================================================
def busiestTimes():
    #Adds just the dates to a dataframe
    datesFrame = logData[41]

    #Removes times for easier searching. Implementing times is the same method, just with 12:whatever in brackets
    for i in datesFrame.index:
        dateString = datesFrame.loc[i]
        dateString = dateString[0:10]
        datesList.append(dateString)

    #Turns it into a dataframe with column "date"
    newDatesFrame = pd.DataFrame(np.array([datesList]).T)
    newDatesFrame.columns = ['Date']

    #Determines top 5 most common dates and returns it
    bTimes = newDatesFrame['Date'].value_counts()[:].sort_values(ascending=False)
    return bTimes
#===========================================================================================================================
bTimes = busiestTimes()
bTimes.to_csv('busiestTimes.csv', index = True, header = False)
bTimesStr = bTimes.to_string()

#hide main TK window
#alert_window = tk.Tk()
#alert_window.withdraw() 

#show user their busiest times
#messagebox.showinfo("Busiest Times on the Network", bTimesStr)
#===========================================================================================================================
#Description: Finds null data and stores it.  Removes nulls from dataframe used in processing
#===========================================================================================================================

#Makes a list of initial indices in the dataframe. Will be used for later index matching.
initialIndexes = []
for row in logData.index:
    initialIndexes.append(row)  

#Makes an empty list of indexes that are dropped. Will be used for later index matching.
dropIndexes = []

#This method adapted from: https://www.geeksforgeeks.org/find-location-of-an-element-in-pandas-dataframe-in-python/
#===========================================================================================================================
def findNulls (dataframe, item):
    positions = []
    result = dataframe.isin([item])
    series = result.any()
    columnNames = list(series[series == True].index)
    
    for col in columnNames: 
        rows = list(result[col][result[col] == True].index)
        for row in rows: 
            positions.append((row, col))
            #Updates list of dropped indexes
            dropIndexes.append(row)
    return positions
#===========================================================================================================================

#Drops columns containing only null values
logData = logData.dropna(axis=1, how='all')

#Determines where null values are in the dataframe
nullValues = logData.isnull()


#Stores the locations of these null values
listOfNulls = findNulls(nullValues, True)
#for i in range(len(listOfNulls)):
    #print('Position ', i, ' (Row index , Column Name) : ', listOfNulls[i])

#Exports a CSV of the locations of Null Values, as long as some were found.
nullsDF = DataFrame(listOfNulls)

if len(nullsDF.columns) != 0:
    nullsDF.columns = ['row','column']
    nullsDF.to_csv('nullValues.csv', index = False, header = False)

alert_window = tk.Tk()
alert_window.withdraw()
messagebox.showinfo("File Created", "nullValues.csv has been created in your project directory")
    
#Rows with null values are then deleted from the dataframe because they cannot be used for machine learning/anomaly detection
logData = logData.dropna()
#===========================================================================================================================

#Description: Asks for desired timeframe from user.  Selects corresponding records. Default is the most recent 20k records.
#===========================================================================================================================

#Assumes timestamp is in the ISO 8601 aka yyyy-mm-ddThh:mm:ssZ, where T stands for time and Z is time zone
#Search for format in first 10 records to determine the column that contains the timestamp
#Checks to see which column is the timeframe column
for x in sample:
    if sample[x].dtype==object:
        timeRows = sample[x].str.contains(pat='[0-9]{4}-[0-9]{2}-[0-9]{2}')
        for y in timeRows:
            if y == True:
                timeCol = x
            else:
                timeCol = None

#Get timeframe from user: prompt it to be in the ISO format 
#Assuming in our timezone, as that is where our company is located
#userETF = input("Enter the earliest date in the form yyyy-mm-ddThh:mm:ssZ: ")
#userRTF = input("Enter the most recent date in the form yyyy-mm-ddThh:mm:ssZ: ")

#https://stackoverflow.com/questions/15495559/taking-input-from-the-user-in-tkinter
#https://datatofish.com/entry-box-tkinter/

#function to get the timeframes the user enters into the GUI
def getInfo():
    global userETF 
    global userRTF
    userETF = firstInput.get() 
    userRTF = secondInput.get()
    #print(userETF)
    #print(userRTF)

def onExit():
    enter_time.quit()
    enter_time.destroy()
    
#create new TK object and set the size of the window
enter_time = Tk()
enter_time.geometry('700x300')
enter_time.title('Enter Timeframe')
enter_time.protocol("WM_DELETE_WINDOW", onExit)

#create new canvas in order to adjust placing of objects in the window
canvas = tk.Canvas(enter_time)
#makes sure canvas takes up no more space than what is needed
canvas.pack()

#label to tell user to enter first part of timeframe; place label on window
label1 = tk.Label(enter_time, text="Enter the earliest date in the form yyyy-mm-ddThh:mm:ssZ: ")
canvas.create_window(200, 25, window=label1)

#Entry box for first part of timeframe -> lets user enter a single string; place entry box on window
firstInput = tk.Entry(enter_time)
canvas.create_window(200, 50, window=firstInput)

#label to tell user to enter second part of timeframe; place label on window
label2 = tk.Label(enter_time, text="Enter the most recent date in the form yyyy-mm-ddThh:mm:ssZ: ")
canvas.create_window(200, 75, window=label2)

#Entry box for second part of timeframe -> lets user enter a single string; place entry box on window                
secondInput = tk.Entry(enter_time) 
canvas.create_window(200, 100, window=secondInput)

#user will click the submit button to store their input
submit = Button(enter_time,text="Submit",command=getInfo)
canvas.create_window(200, 125, window=submit)

label3 = tk.Label(enter_time, text="Click submit and then close window")
canvas.create_window(200, 150, window=label3)

exitBtn = Button(enter_time, text="Exit", command=onExit)
canvas.create_window(200, 175, window=exitBtn)

#keeps window open for user to be able to enter their data
enter_time.mainloop()

#===========================================================================================================================

def pickRecords(logData, numRows): 
    update_window = tk.Tk()
    update_window.withdraw() 
    messagebox.showinfo("User update", "We will pick the most recent 20k records for you: this may take a minute.")

    #the most recent rows will be at the bottom bc they were entered last, so we use the last 20K rows
    #if the size of the file is less than 20k records, we select the whole file
    if numRows <= 20000 and numRows != 0: 
        sRows = numRows
        selectedDF = logData.tail(sRows)
        logData = selectedDF
    else:
        sRows = 20000
        selectedDF = logData.tail(sRows)
        logData = selectedDF
    return logData

#===========================================================================================================================        

#create empty list for indices of unwanted records not within the timeframe to be added
dropLocs = []

#get number of records 
numRows = len(logData.index)

#===========================================================================================================================
#if the file does contain timestamps
if timeCol != None:
    timeCol = int(timeCol)
    
    #match the timestamp pattern to user input
    if re.match("[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z",userETF) and re.match("[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z",userRTF):
        #print("You have selected a timeframe of: " + userETF + " to " + userRTF)
        
        if not(userETF > userRTF): 
            msg_window = tk.Tk()
            msg_window.withdraw() 
            messagebox.showinfo("User Update", "Searching all records. This may take a minute. ")
            
            for x in range(numRows):
                if timeCol != None:
                    #if record is not in timeframe, add its index to the drop list
                    if not(logData.iloc[x,timeCol] >= userETF) or not(logData.iloc[x,timeCol] <= userRTF):
                        dropLocs.append(x)
                    
        #if the user entered the range of time backwards, we choose for them
        else:
            msg_win = tk.Tk()
            msg_win.withdraw() 
            messagebox.showinfo("User Update", "The dates entered were switched.")
            
            logData = pickRecords(logData, numRows)

    #if the user includes a timestamp format that is not supported        
    else:
        message_window = tk.Tk()
        message_window.withdraw() 
        messagebox.showinfo("User Update", "Dates entered in an incorrect format.")
            
        logData = pickRecords(logData, numRows)
        
#if the file does not contain timestamps, we choose the records for them
else:
    ud_window = tk.Tk()
    ud_window.withdraw() 
    messagebox.showinfo("User Update", "Your log data does not appear to contain timestamps.")
        
    logData = pickRecords(logData, numRows)
#===========================================================================================================================

#Drops rows based on timeframe
if dropLocs != []:
    for x in dropLocs:
        #Updates list of dropped indices
        dropIndexes.append(x)
        #Drops indices
        logData.drop([x], inplace = True)
elif len(dropLocs) == numRows:
    mg_box = tk.Tk()
    mg_box.withdraw() 
    messagebox.showinfo("User Update", "No records in range.")
    logData = pickRecords(logData, numRows)
else:
    msg_box = tk.Tk()
    msg_box.withdraw() 
    messagebox.showinfo("User Update", "All records are in range. ")
            
#===========================================================================================================================

if timeCol != None:
    logData = logData.drop([timeCol], axis = 1)

#Sorts the list of dropped rows for later use
dropIndexes.sort()
#===========================================================================================================================
#This method taken from method #4 in: https://www.geeksforgeeks.org/python-find-missing-numbers-in-a-sorted-list-range/
#Description: Takes the list of dropped indexes and reverses it to make a list of included indexes
#===========================================================================================================================
def find_missing(dropIndexes):
    start = 0
    end = dropIndexes[-1]
    return sorted(set(range(start, end + 1)).difference(dropIndexes))
#===========================================================================================================================
includedIndexes = find_missing(dropIndexes)

stillThere = pd.DataFrame(np.array([includedIndexes]).T)
stillThere.to_csv('stillThere.csv', index = False, header = False)

#Description: Removes IP Addresses from the dataframe that will be used in processing
#===========================================================================================================================

ipList = []

#Checks to see which columns contain IP addresses, if there are any, then drops them.
#===========================================================================================================================

for x in sample:
    if sample[x].dtype==object:
        ipRows = sample[x].str.contains(pat='[0-9]+(?:\.[0-9]+){3}')
        for y in ipRows:
            if y == True:
                ipList.append(x)
                
#===========================================================================================================================

#actually drops the column if said column exists
if not ipList:
    m_window = tk.Tk()
    m_window.withdraw() 
    messagebox.showinfo("User Update", "Data contains no IP Adresses.")
else:
    logData = logData.drop(ipList, axis=1)   
    
#renumbers columns accordingly
logData.columns = range(logData.shape[1])

#Description: Finds all non-numerical columns and normalizes them. It does this by taking a column's possible items and 
#creating corresponding columns. For example, a column with values of either TCP or UDP would them become two columns, one
#for TCP and one for UDP.  If that row has that connection type, a 1 is placed as the value. If it does not, then a 0 is
#placed. Thus keeping the integrity of the data.
#Also normalizes the numerical data.

#===========================================================================================================================

#Finds which columns are not numerical and creates a list to hold their indices
logData_dtypes = np.array(logData.dtypes)
logData_numericDtypes= [x.kind in 'bifc' for x in logData_dtypes]
catColumns = []

#Adds indices to list catColumns
for i, j in enumerate(logData_numericDtypes):
    if j == False:
        catColumns.append(i)

#Creates an empty dataframe to hold dummy values
dummiesDF = pd.DataFrame()

#Makes dummy values/columns for the columns with nominal attributes whose indices are held in catColumns
for i in logData:
    if i in catColumns:
        dummiesDF = pd.concat([dummiesDF, pd.get_dummies(logData[i])], axis=1)

#Appends dummy columns to dataset
numericLogData = pd.concat([logData, dummiesDF], axis=1)

#Removes columns that have been dummied out
numericLogData = numericLogData.drop(columns = catColumns)

#Normalizes data between 0 and 1
d = preprocessing.normalize(numericLogData)
normLogData = pd.DataFrame(d)

#Exports the dataframe as a CSV file
normLogData.to_csv('normalizedData.csv', index = False, header = False) 

m_box = tk.Tk()
m_box.withdraw() 
messagebox.showinfo("File Created", "normalizedData.csv has been created in your project directory")