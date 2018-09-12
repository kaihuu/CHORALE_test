import plotly.plotly as py
import plotly
import plotly.graph_objs as go
import os
import math
from DBAccessor import DBAccessor as dbac
import numpy as np

def sturgesFormula(n):
    return round(1 + math.log2(n))


api_key = os.environ["PLOTLY_API_KEY"]
plotly.tools.set_credentials_file(username='kaihuu', api_key=api_key)

#クエリ実行
result = dbac.ExecuteQueryFromList(dbac.QueryString(), [306])
#ビン数計算
Num_of_bin = sturgesFormula(len(result))

npresult = np.array(result)

print(npresult)

max = np.amax(npresult, axis=0)
min = np.amin(npresult, axis=0)

print(max)
print(min)
print(max - min)

print(Num_of_bin)

x = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
y = ['Morning', 'Afternoon', 'Evening']
z = [[1, 20, 30, 50, 1], [20, 1, 60, 80, 30], [30, 60, 1, -10, 20]]


trace = go.Heatmap(z=z, x=x, y=y)
data=[trace]
#py.plot(data, filename='CHORALE')