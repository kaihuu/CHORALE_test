import plotly.plotly as py
import plotly.graph_objs as go
import plotly.offline as offline
from DBAccessor import DBAccessor as dbac
import numpy as np
from datetime import datetime,timedelta
import os
import googlemaps

def getTrace(semanticLinkID):
    #result = dbac.ExecuteQueryFromList(dbac.QueryStringGetLatencyTestTime(), [testID])
    endpoints = dbac.ExecuteQueryFromList(dbac.QueryStringGetEndPoints(), [semanticLinkID])
    
    now= datetime.now()

    matrix = getMatrix(now, str(endpoints[1][2]), str(endpoints[1][3]),
     str(endpoints[0][2]), str(endpoints[0][3]))
    
    duration = matrix["rows"][0]["elements"][0]["duration_in_traffic"]["value"]
    print(duration)
    print(type(duration))
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

def getMatrix(now, startLatitude, startLongitude, endLatitude, endLongitude):
    matrix_result = gmaps.distance_matrix((startLatitude, startLongitude),
                                        (endLatitude, endLongitude),
                                        mode="driving",
                                        traffic_model = "best_guess",
                                        departure_time=now
                                        )

    return matrix_result


#API前準備
api_key = os.environ["GOOGLE_MAP_API_KEY"]
gmaps = googlemaps.Client(key=api_key)



data = [getTrace(207)]

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