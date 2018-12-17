import plotly.plotly as py
import plotly.graph_objs as go
import googlemaps
import plotly.offline as offline
import numpy as np

x0 = np.random.randn(500)
x1 = np.random.randn(500)

trace0 = go.Histogram(
    x=x0
)
trace1 = go.Histogram(
    x=x1
)
data = [trace0, trace1]
layout = go.Layout(barmode='stack')
fig = go.Figure(data=data, layout=layout)

offline.plot(fig, filename='stacked histogram.html')
