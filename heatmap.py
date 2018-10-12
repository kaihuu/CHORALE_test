import plotly.plotly as py
import plotly
import plotly.graph_objs as go
import os
import math
from DBAccessor import DBAccessor as dbac
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt



def sturgesFormula(n):
    return round(1 + math.log2(n))

np.random.seed(0)

#クエリ実行
result = dbac.ExecuteQueryFromList(dbac.QueryString(), [306])
#ビン数計算
Num_of_bin = sturgesFormula(len(result))

npresult = np.array(result, dtype='float')

print(npresult)

max = np.amax(npresult, axis=0)
min = np.amin(npresult, axis=0)

print(max)
print(min)
print(Num_of_bin)

l = (max - min) / Num_of_bin
print(l)

xax = np.array([])
for i in range(Num_of_bin):
    print(min[0] + float(i) * l[0])
    xax = np.append(xax, [min[0] + float(i) * l[0]])


print(xax)

uniform_data = np.random.rand(100, 100)
#sns.heatmap(npresult)
#plt.show()