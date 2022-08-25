from asyncore import read
from distutils.command import clean
from pathlib import Path
from re import X
import os
import pandas as pd
import matplotlib.pyplot as plt
import glob
import numpy as np
import matplotlib.ticker as ticker
from bokeh.plotting import figure, save, gridplot, output_file

#path = r'/Users/tylerreinert/Desktop/MM210504 FCD files'
path = input("Enter your folder name: ")            #prompting user for folder path
reading = (r'{}').format(path)                      #reading files in folder to list 


filenames = glob.glob(reading + "/*.fcd")

fileDictionary = {}

def plotMechs(x, y, xtitle, ytitle, fileTitle):
     
    plt.scatter(x,y, marker=".", s=1)

    plt.xlabel(xtitle, fontsize=15)
    plt.ylabel(ytitle, fontsize=15)
    plt.title(f" {fileTitle} ", fontsize=20,pad=10)

    plt.grid(True)
    plt.show()


def fileParser(filename):
    cleanData = []
    fileTitle = filename[filename.rindex('/')+1:]
    with open(filename, "r", encoding='latin_1') as file:
        for line in file:
            dataInfo = line.strip().split('\t')
            if len(dataInfo) > 10:
                    cleanData.append(dataInfo)
    if cleanData[0][0] == "Time (Sec)" :  #mainly for QA 
        fileDictionary[fileTitle] = pd.DataFrame(cleanData[1:], columns=cleanData[0])
        occurence = fileDictionary[fileTitle]

        print(occurence)


        fileTitle = filename[filename.rindex('/')+1:]
        timeTitle = occurence.columns[0]
        voltageTitle = occurence.columns[5]
        currentDensityTitle = occurence.columns[2]
        powerDensityTitle = occurence.columns[4]

        
        

        if "OCV" in filename:
            x = occurence['Time (Sec)']
            x = np.array(list(map(float, x)))
            y = occurence['E_Stack (V)']
            y = np.array(list(map(float, y)))
            plotMechs(x, y,timeTitle, voltageTitle, fileTitle)

        elif "Cond" in filename:
            x = (occurence['Time (Sec)'])
            x = np.array(list(map(float, x)))
            y = occurence['I (mA/cm²)']
            y = np.array(list(map(float, y)))
            plotMechs(x, y,timeTitle,currentDensityTitle, fileTitle)

        elif "SC" in filename:
            x = (occurence['I (mA/cm²)'])
            y = occurence['E_Stack (V)']
            z = occurence['Power (mW/cm²)']
            x = np.array(list(map(float, x)))
            y = np.array(list(map(float, y)))
            z = np.array(list(map(float, z)))
            plt.yticks(np.arange(0, 1.1, 0.1))
            plotMechs(x, y, currentDensityTitle,voltageTitle, fileTitle)
            plotMechs(x, z, currentDensityTitle, powerDensityTitle, fileTitle)



for filename in filenames:
    fileParser(filename)

#print(fileDictionary)



for testRun in fileDictionary:
    writer = pd.ExcelWriter(f"{testRun}")
    fileDictionary[testRun].to_excel(writer, sheet_name=testRun)


# next steps
# get all plots to show at once, not huge deal for end product
# make figure consisting of all plots
# get titles and axis titles displayed, use function
# make plots interactive
# make plots more readable, get maxima and minima on graph


# need to set up website for form submission, allow for folders to be uploaded
# set up backend database to store and organize files
# ----> figure out what type of file is being generated, how can it be stored...
# make system for accessing specific files by user, date, cell size, test type, run#
# design sign-in system
# get this thing hosted on a server
