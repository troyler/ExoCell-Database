from asyncore import read
from distutils.command import clean
import originpro as op
import pandas as pd
import matplotlib.pyplot as plt
import glob
import numpy as np
import matplotlib.ticker as ticker
from bokeh.plotting import figure, save, gridplot, output_file

path = r'C:\Users\trein\Desktop\ExoCell\Data for ExoCell\MM210918'

filenames = glob.glob(path + '/*.fcd')

cleanData = []

for filename in filenames:
    if "09_29_21_MM210918_OCV1_DRY H2_30 psi_serpentine-2_TFFC_1" in filename:
        print(filename)
        with open(filename,"r") as file:
            for line in file:
                dataInfo = line.strip().split('\t')
                if len(dataInfo) > 10:

                    cleanData.append(dataInfo)


df = pd.DataFrame(cleanData[1:], columns = cleanData[0])
print(cleanData[0])
print(df)

y= df['E_Stack (V)']
y = np.array(list(map(float, y)))
x= np.array(df['Time (Sec)'])

# corresponding y axis values
  
# plotting the points 
plt.scatter(x,y,marker = ".")
plt.xticks(np.arange(0, (len(x)+1), 8))
plt.show()
#

