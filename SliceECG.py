import plotly.plotly as py
import plotly.graph_objs as go
import plotly.offline as offline
from DBAccessor import DBAccessor as dbac
import numpy as np

def getTrace(testID, name):
    #result = dbac.ExecuteQueryFromList(dbac.QueryStringGetLatencyTestTime(), [testID])
    yresult = np.array([1.0,1.11,1.21,1.1,1.2])
    xresult = np.full(5,"Convert Loss")

    #npresult = np.array(result)

    trace0 = go.Scatter(
        x=xresult,
        #y = npresult[:, 3:4].flatten(),
        y=yresult,
        mode='markers'
    )
    return trace0


data = [getTrace(85, "N=1")]

layout = go.Layout(
    xaxis=dict(tickfont=dict(size=20)),
    yaxis=dict(tickfont=dict(size=20))
)


fig = go.Figure(data=data, layout=layout)

offline.plot(fig, "test1_500.html")

#data = [getTrace(69, "N=10"),getTrace(76, "N=20")
#, getTrace(81, "N=50"), getTrace(79, " N=100"), getTrace(83, "N=500")]

#fig = go.Figure(data=data)

#offline.plot(fig, "test10_500.html")