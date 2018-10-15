import plotly.plotly as py
import plotly
import plotly.graph_objs as go
import os
import math
from DBAccessor import DBAccessor as dbac
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd



def sturgesFormula(n):
    return round(1 + math.log2(n))

def generateBinData(data):
    #ビン数計算
    Num_of_bin = sturgesFormula(len(data))
    npresult = np.array(data, dtype='float')
    
    max = np.amax(npresult, axis=0)
    min = np.amin(npresult, axis=0)
    
    l = (max - min) / Num_of_bin

    xax = generateAxisData(Num_of_bin, min[0], l[0])
    yax = generateAxisData(Num_of_bin, min[1], l[1])

    return xax, yax, npresult

def generateAxisData(Num_of_bin, min, length):
    ax = np.array([])
    for i in range(Num_of_bin):
        ax = np.append(ax, [min + float(i) * length])
    return ax

def generateHeatmapData(Num_of_bin, np, xax, yax):
    df_result = pd.DataFrame(np)
    for i in range(Num_of_bin):
        for t in range(Num_of_bin):
            df_af = df_result[(df_result[0] >= xax[i]) & (df_result[0] < xax[i]) 
            & (df_result[1] >= yax[t]) & (df_result[1] < yax[t])]
            len(df_af)

    return result


np.random.seed(0)

#クエリ実行
result = dbac.ExecuteQueryFromList(dbac.QueryString(), [306])

xax, yax, npresult = generateBinData(result)

df_result = pd.DataFrame(npresult)

df_af = df_result[(df_result[0] >= xax[3]) & (df_result[0] < xax[4]) & (df_result[1] >= yax[3]) & (df_result[1] < yax[4])]
print(df_af)
print(len(df_af))


uniform_data = np.random.rand(100, 100)
#sns.heatmap(npresult)
#plt.show()