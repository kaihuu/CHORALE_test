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


def matplotlib_to_plotly(cmap, pl_entries):
    h = 1.0/(pl_entries-1)
    pl_colorscale = []
    print(h)
    for k in range(pl_entries):
        C = list(map(np.uint8, np.array(cmap[:3])*k*h*255))

        pl_colorscale.append([k*h, 'rgb'+str((C[0], C[1], C[2]))])

    return pl_colorscale

def get_cmap():
    magma_cmap = matplotlib.cm.get_cmap('magma')
    viridis_cmap = matplotlib.cm.get_cmap('viridis')

    viridis_rgb = []
    magma_rgb = []
    norm = matplotlib.colors.Normalize(vmin=0, vmax=255)

    for i in range(0, 255):
       k = matplotlib.colors.colorConverter.to_rgb(magma_cmap(norm(i)))
       magma_rgb.append(k)

    for i in range(0, 255):
       k = matplotlib.colors.colorConverter.to_rgb(viridis_cmap(norm(i)))
       viridis_rgb.append(k)
    
    magma = matplotlib_to_plotly(magma_rgb, 255)
    viridis = matplotlib_to_plotly(viridis_rgb, 255)

    return magma,viridis

def generateHeatmapData(Num_of_bin, df_result, xbin, ybin):
    result = np.empty((0, Num_of_bin), int)
    for i in range(Num_of_bin):
        arr = np.empty((0, Num_of_bin), int)
        for t in range(Num_of_bin):
            df_af = df_result[(df_result[0] >= xbin[i]) & (df_result[0] < xbin[i + 1]) 
            & (df_result[1] >= ybin[t]) & (df_result[1] < ybin[t + 1])]
            arr = np.append(arr, len(df_af))      

        result = np.append(result, [arr], axis=0)
        
    return result

def sturgesFormula(n):
    return round(1 + math.log2(n))

def generateBinData(data):
    #ビン数計算
    Num_of_bin = sturgesFormula(len(data))
    npresult = np.array(data, dtype='float')


    df_result = pd.DataFrame(npresult)

    Q1 = df_result.quantile(.25)
    Q3 = df_result.quantile(.75)
    IQR = Q3 - Q1
    print(IQR)
    maxthereshold = Q3 + 1.5 * IQR
    minthereshold = Q1 - 1.5 * IQR
    print(minthereshold)
    print(df_result)
    df_result = df_result[(df_result[0] >= minthereshold[0]) & (df_result[0] <= maxthereshold[0])
                & (df_result[1] >= minthereshold[1]) & (df_result[1] <= maxthereshold[1])]
    print(df_result)
    max = np.amax(npresult, axis=0)
    min = np.amin(npresult, axis=0)

    if max[0] >= maxthereshold[0]:
        max[0] = maxthereshold[0]
    
    if max[1] >= maxthereshold[1]:
        max[1] = maxthereshold[1]

    if min[0] <= minthereshold[0]:
        min[0] = minthereshold[0]
    
    if min[1] <= minthereshold[1]:
        min[1] = minthereshold[1]
    

    l = (max - min) / Num_of_bin
    xbin = generateEachBinData(Num_of_bin, min[0], l[0])
    ybin = generateEachBinData(Num_of_bin, min[1], l[1])

    return xbin, ybin, df_result, Num_of_bin

def generateEachBinData(Num_of_bin, min, length):
    abin = np.array([])
    for i in range(Num_of_bin + 1):
        abin = np.append(abin, [min + float(i) * length])
    return abin

def generateAxisData(xbin, ybin, Num_of_bin):
    xax = []
    yax = []
    for i in range(Num_of_bin):
        xax.append('{:.2e}'.format((xbin[i] + xbin[i+1]) / 2))
        yax.append('{:.2e}'.format((ybin[i] + ybin[i+1]) / 2))

    return xax, yax

def showHeatmapGraph(semanticLinkID, tripDirection):
    #クエリ実行
    result = dbac.ExecuteQueryFromList(dbac.QueryString(), [semanticLinkID, tripDirection])
    semanticInfo = dbac.ExecuteQueryFromList(dbac.QueryStringGetSemantics(), [semanticLinkID, tripDirection])

    xbin, ybin, df_result, Num_of_bin = generateBinData(result)

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

    fig["layout"].setdefault("title", str(semanticInfo[0][0]) + "  " + semanticInfo[0][1])
    fig["layout"].setdefault("titlefont", dict(size=30))

    for i in range(Num_of_bin * Num_of_bin):
        fig["layout"]["annotations"][i]["font"].setdefault("size", 16)

    fig["layout"].setdefault("margin", dict(l=100))

    fig["layout"]["xaxis"].setdefault("tickfont", dict(size=20))
    fig["layout"]["yaxis"].setdefault("tickfont", dict(size=20))

    fig["layout"]["xaxis"].setdefault("title", "Elapsed Time[s]")
    fig["layout"]["yaxis"].setdefault("title", "LostEnergy[kWh]")

    fig["layout"]["xaxis"].setdefault("titlefont", dict(size=20))
    fig["layout"]["yaxis"].setdefault("titlefont", dict(size=20))

    fig["layout"]["yaxis"].setdefault("tickformat", ".1e")

    fig["layout"]["xaxis"].pop("side")
    fig["layout"]["yaxis"].pop("ticksuffix")
    fig["layout"]["xaxis"].pop("dtick")
    fig["layout"]["yaxis"].pop("dtick")

    offline.plot(fig, filename="CHORALE" + str(semanticLinkID) + ".html")

#outward
for i in range(304, 327):
    showHeatmapGraph(i, "outward")
#homeward
for i in range(305, 328):
    showHeatmapGraph(i, "homeward")