import plotly.plotly as py
import plotly.graph_objs as go
import plotly.offline as offline
from DBAccessor import DBAccessor as dbac
import numpy as np

def getTrace(testID, name):
    #result = dbac.ExecuteQueryFromList(dbac.QueryStringGetLatencyTestTime(), [testID])
    result = np.array([1.0,1.1,1.2,1.1,1.2])

    #npresult = np.array(result)

    trace0 = go.Box(
        #y = npresult[:, 3:4].flatten(),
        y=result,
        name = name,
        #jitter = 0.3,
        #pointpos = -1.8,
        boxpoints = 'all',
        #marker = dict(
        #    color = 'rgb(7,40,89)'),
        #line = dict(
        #    color = 'rgb(7,40,89)')
    )
    return trace0


data = [getTrace(85, "N=1"), getTrace(86, "N=2"), getTrace(87, "N=3"), getTrace(88, "N=4")
, getTrace(89, "N=5"),getTrace(90, "N=10"),getTrace(91, "N=15")
, getTrace(92, "N=20"), getTrace(93, " N=50"), getTrace(94, "N=100") , getTrace(95, "N=500")
 , getTrace(97, "N=1000")]

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