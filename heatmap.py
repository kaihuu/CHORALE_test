import math
import os

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objs as go
import plotly.offline as offline
import seaborn as sns
from DBAccessor import DBAccessor as dbac
from matplotlib import cm
import plotly.io as pio
import plotly.plotly as py


def generateHeatmapData(Num_of_bin, df_result, xbin, ybin):
    #print(df_result)
    result = np.empty((0, Num_of_bin), int)
    for i in range(Num_of_bin):
        arr = np.empty((0, Num_of_bin), int)
        for t in range(Num_of_bin):
            if t == Num_of_bin - 1 or i == Num_of_bin - 1:
                #print(str(xbin[i]) + "<= x <= " + str(xbin[i+1]) +"  " + str(ybin[t]) + "<= y <=" + str(ybin[t+1]))
                df_af = df_result[(df_result[0] >= xbin[i]) & (df_result[0] <= xbin[i + 1]) 
                & (df_result[1] >= ybin[t]) & (df_result[1] <= ybin[t + 1])]
                arr = np.append(arr, len(df_af))
                #print(df_af)
                #print()
            else:
                #print(str(xbin[i]) + "<= x < " + str(xbin[i+1]) + "  " + str(ybin[t]) + "<= y <" + str(ybin[t+1]))
                df_af = df_result[(df_result[0] >= xbin[i]) & (df_result[0] < xbin[i + 1]) 
                & (df_result[1] >= ybin[t]) & (df_result[1] < ybin[t + 1])]
                arr = np.append(arr, len(df_af))
                #print(df_af)
                #print()     

        result = np.append(result, [arr], axis=0)
        
    return result.T

def sturgesFormula(n):
    return round(1 + math.log2(n))

def generateBinData(data, Num_of_bin):
    #ビン数計算
    #Num_of_bin = sturgesFormula(len(data))

    npresult = np.array(data, dtype='float')


    df_result = pd.DataFrame(npresult)

    Q1 = df_result.quantile(.25)
    Q3 = df_result.quantile(.75)
    IQR = Q3 - Q1
    #print(IQR)
    maxthereshold = Q3 + 1.5 * IQR
    minthereshold = Q1 - 1.5 * IQR
    #print(minthereshold)
    #print(df_result)
    #df_result = df_result[(df_result[0] >= minthereshold[0]) & (df_result[0] <= maxthereshold[0])
    #            & (df_result[1] >= minthereshold[1]) & (df_result[1] <= maxthereshold[1])]
    #print(df_result)
    max = np.amax(npresult, axis=0)
    min = np.amin(npresult, axis=0)

    #if max[0] >= maxthereshold[0]:
    #    max[0] = maxthereshold[0]
    
    #if max[1] >= maxthereshold[1]:
    #    max[1] = maxthereshold[1]

    #if min[0] <= minthereshold[0]:
    #    min[0] = minthereshold[0]
    
    #if min[1] <= minthereshold[1]:
    #    min[1] = minthereshold[1]
    
    l = (max - min) / Num_of_bin
    xbin = generateEachBinData(Num_of_bin, min[0], l[0])
    ybin = generateEachBinData(Num_of_bin, min[1], l[1])
    return xbin, ybin, df_result

def generateEachBinData(Num_of_bin, min, length):
    abin = np.array([])
    for i in range(Num_of_bin + 1):
        abin = np.append(abin, [min + float(i) * length])
    return abin

def generateAxisData(xbin, ybin, Num_of_bin):
    xax = []
    yax = []
    for i in range(Num_of_bin):
        xax.append('{:.3e}'.format((xbin[i] + xbin[i+1]) / 2))
        yax.append('{:.3e}'.format((ybin[i] + ybin[i+1]) / 2))

    return xax, yax

def showHeatmapGraph(semanticLinkID, tripDirection, Num_of_bin, imageFlag=True):
    #クエリ実行
    result = dbac.ExecuteQueryFromList(dbac.QueryString(), [semanticLinkID, tripDirection])
    semanticInfo = dbac.ExecuteQueryFromList(dbac.QueryStringGetSemantics(), [semanticLinkID])

    xbin, ybin, df_result= generateBinData(result, Num_of_bin)
    heatmapData = generateHeatmapData(Num_of_bin, df_result, xbin, ybin)

    xax, yax = generateAxisData(xbin, ybin, Num_of_bin)

    hoverlabel = dict(font=dict(size=20))
    colorbar = dict(tickfont=dict(size=20))


    fig = ff.create_annotated_heatmap(x=xax, y=yax, z=heatmapData, colorscale = "Jet", 
    zsmooth = 'best', showscale = True, showlegend=True, hoverlabel=hoverlabel,
    colorbar=colorbar)


    axis_layout = dict(
        tickfont=dict(
            size=20
        )
    )

    layout = dict(
        xaxis=axis_layout,
        yaxis=axis_layout
        )
    #print(fig)
    fig["layout"].title = str(semanticInfo[0][0]) + "  " + semanticInfo[0][1] + "  " + tripDirection
    #fig["layout"].setdefault("title", str(semanticInfo[0][0]) + "  " + semanticInfo[0][1] + "  " + tripDirection)
    
    fig["layout"].titlefont = dict(size=30)
    #fig["layout"].setdefault("titlefont", dict(size=30))


    for i in range(Num_of_bin * Num_of_bin):
        fig["layout"]["annotations"][i]["font"].size = 16
    #for i in range(Num_of_bin * Num_of_bin):
    #    fig["layout"]["annotations"][i]["font"].setdefault("size", 16)
    fig["layout"].margin = dict(l=100)
    #fig["layout"].setdefault("margin", dict(l=100))


    fig["layout"]["xaxis"].tickfont = dict(size=20)
    fig["layout"]["yaxis"].tickfont = dict(size=20)
    #fig["layout"]["xaxis"].setdefault("tickfont", dict(size=20))
    #fig["layout"]["yaxis"].setdefault("tickfont", dict(size=20))


    fig["layout"]["xaxis"].title = "Elapsed Time[s]"
    fig["layout"]["yaxis"].title = "LostEnergy[kWh]"
    #fig["layout"]["xaxis"].setdefault("title", "Elapsed Time[s]")
    #fig["layout"]["yaxis"].setdefault("title", "LostEnergy[kWh]")


    fig["layout"]["xaxis"].titlefont = dict(size=20)
    fig["layout"]["yaxis"].titlefont = dict(size=20)
    #fig["layout"]["xaxis"].setdefault("titlefont", dict(size=20))
    #fig["layout"]["yaxis"].setdefault("titlefont", dict(size=20))

    fig["layout"]["yaxis"].tickformat = ".1e"
    #fig["layout"]["yaxis"].setdefault("tickformat", ".1e")
    #print(fig)

    fig["layout"]["xaxis"].side = None
    fig["layout"]["yaxis"].ticksuffix = None
    fig["layout"]["xaxis"].dtick = None
    fig["layout"]["yaxis"].dtick = None
    
    #fig["layout"]["xaxis"].pop("side")
    #fig["layout"]["yaxis"].pop("ticksuffix")
    #fig["layout"]["xaxis"].pop("dtick")
    #fig["layout"]["yaxis"].pop("dtick")

    #print(fig)
    offline.plot(fig, filename="CHORALE" + str(semanticLinkID) + tripDirection + ".html")
    if imageFlag:
        fig["layout"].width = 1280
        fig["layout"].height = 960
        pio.write_image(fig, "images/CHORALE" + str(semanticLinkID) + tripDirection + str(Num_of_bin) + ".png")
        pio.write_image(fig, "images/CHORALE" + str(semanticLinkID) + tripDirection + str(Num_of_bin) + ".svg")


#outward
#for i in range(332, 339):
#    showHeatmapGraph(i, "outward")
#homeward
#for i in reversed(range(333, 339)):
#    showHeatmapGraph(i, "homeward")

#showHeatmapGraph(340, "homeward")

if not os.path.exists('images'):
    os.mkdir('images')

id = 332
tripdirection = "outward"
imageFlag = False

showHeatmapGraph(id, tripdirection, 5, imageFlag)
showHeatmapGraph(id, tripdirection, 10, imageFlag)
showHeatmapGraph(id, tripdirection, 20, imageFlag)
showHeatmapGraph(id, tripdirection, 6, imageFlag)
showHeatmapGraph(id, tripdirection, 7, imageFlag)
showHeatmapGraph(id, tripdirection, 8, imageFlag)
showHeatmapGraph(id, tripdirection, 9, imageFlag)