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
from plotly import tools

def showHeatmapGraph(semanticLinkID, tripDirection, imageFlag=True):
    #クエリ実行
    result = dbac.ExecuteQueryFromList(dbac.QueryStringforECG(), [semanticLinkID, tripDirection])

    npresult = np.array(result, dtype='float')
    
    nptime = npresult[:, 0:1].flatten()
    nplost = npresult[:, 1:2].flatten()
    npconvert = npresult[:, 2:3].flatten()
    npregene = npresult[:, 3:4].flatten()
    npair = npresult[:, 4:5].flatten()
    nproll = npresult[:, 5:6].flatten()
    nptripid = npresult[:, 6:7].flatten()

    cmax = np.amax(npresult[:, 2:6])
    print(cmax)

    trace1 = go.Scatter(x=nptime, y=nplost, mode='markers',
                marker=dict(size = 16, color=npconvert, colorscale="Jet", cmax=cmax, cmin=0)
                ,text=nptripid)
    trace2 = go.Scatter(x=nptime, y=nplost, mode='markers',
                marker=dict(size = 16, color=npregene, colorscale="Jet", cmax=cmax, cmin=0)
                ,text=nptripid)
    trace3 = go.Scatter(x=nptime, y=nplost, mode='markers',
                marker=dict(size = 16, color=npair, colorscale="Jet", cmax=cmax, cmin=0)
                ,text=nptripid)
    trace4 = go.Scatter(x=nptime, y=nplost, mode='markers', 
                marker=dict(size = 16, color=nproll, colorscale="Jet", cmax=cmax, cmin=0, showscale=True)
                ,text=nptripid)

    fig = tools.make_subplots(rows=2, cols=2, subplot_titles=('CONVERT_LOSS', 'REGENE_LOSS',
                                                          'ENERGY_BY_AIR_RESISTANCE', 'ENERGY_BY_ROLLING_RESISTANCE'))

    fig.append_trace(trace1, 1, 1)
    fig.append_trace(trace2, 1, 2)
    fig.append_trace(trace3, 2, 1)
    fig.append_trace(trace4, 2, 2)

    fig['layout'].update(width = 1280, height = 960, title='ECGs', showlegend=False)
    #fig['layout'].update(title='ECGs', showlegend=False)



    offline.plot(fig, filename="ECGs" + str(semanticLinkID) + tripDirection + ".html")
    if imageFlag:
        fig["layout"].width = 1280
        fig["layout"].height = 960
        #pio.write_image(fig, "images/CHORALE" + str(semanticLinkID) + tripDirection + ".png")
        pio.write_image(fig, "images/CHORALE" + str(semanticLinkID) + tripDirection + ".svg")

showHeatmapGraph(333, "outward")