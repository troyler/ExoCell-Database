from asyncore import read
from distutils.command import clean
from re import X
import originpro as op
import pandas as pd
import matplotlib.pyplot as plt
import glob
import numpy as np
import matplotlib.ticker as ticker
from bokeh.plotting import figure, save, gridplot, output_file

path = r'C:\Users\trein\Desktop\MM210504 FCD files'

filenames = glob.glob(path + '/*.fcd')
print(filenames)


def plotMechs(x, y):
    plt.scatter(x, y, marker=".")
    plt.show()


def fileParser(filename):
    cleanData = []
    print(filename)
    with open(filename, "r") as file:
        for line in file:
            dataInfo = line.strip().split('\t')
            if len(dataInfo) > 10:
                cleanData.append(dataInfo)

    df = pd.DataFrame(cleanData[1:], columns=cleanData[0])
    print(df)

    if "OCV" in filename:
        x = df['Time (Sec)']
        x = np.array(list(map(float, x)))
        y = df['E_Stack (V)']
        y = np.array(list(map(float, y)))
        plotMechs(x, y)

    elif "Cond" in filename:
        x = (df['Time (Sec)'])
        x = np.array(list(map(float, x)))
        y = df['I (mA/cm²)']
        y = np.array(list(map(float, y)))
        plt.yticks(np.arange(0, 1.1, 0.1))
        plotMechs(x, y)

    elif "SC" in filename:
        x = (df['I (mA/cm²)'])
        y = df['E_Stack (V)']
        z = df['Power (mW/cm²)']
        x = np.array(list(map(float, x)))
        y = np.array(list(map(float, y)))
        z = np.array(list(map(float, z)))
        plt.yticks(np.arange(0, 1.1, 0.1))
        plotMechs(x, y)
        plotMechs(x, z)


for filename in filenames:
    fileParser(filename)


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
