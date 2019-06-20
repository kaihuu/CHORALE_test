import plotly.plotly as py
import plotly.graph_objs as go
import plotly.offline as offline
import numpy as np
import json
import pprint
from plotly import tools
import pandas as pd


def maketrace(df, name, side, legend):
    color = 'red'
    if legend == 'Short':
        color = 'blue'
    else :
        color = 'red'
    trace =  {
            "type": 'violin',
            "y": df,
            "legendgroup": legend,
            "name": name,
            "side": side,
            "box": {
                "visible": True
            },
            "meanline": {
                "visible": True
            },
            "line": {
                "color": color
            }
        }
    return trace


#with open('pcpdata1.json', encoding='shift_jis') as f:
with open('pcpzaimokuya.json', encoding='utf-8') as f:
    d = json.load(f)
    #print(d)
    data = json.dumps(d, ensure_ascii=False)
    #print(data)
    df = pd.read_json(data)

#pprint.pprint(d, width=40)

#print(d[0]['ElapsedTime(s)'])

newlist = [df.columns.values[5], df.columns.values[13],df.columns.values[6]]
#print(df)
df1 = df[df['Trips.START_TIME'] <= '2014']
df2 = df[df['Trips.START_TIME'] > '2014']
print(df1)
print(df2)
print(df.columns.values)




fig = tools.make_subplots(rows=1, cols=2)

# df_pass = df[df['Signal2'] == '通過']
# df_pass_corr = df_pass.corr()
# print(df_pass_corr[df.columns.values[1]][df.columns.values[3]])
# print(df_pass_corr[df.columns.values[2]][df.columns.values[4]])
# df_stop = df[df['Signal2'] == '停止']
# df_stop_corr = df_stop.corr()
# print(df_stop_corr[df.columns.values[1]][df.columns.values[3]])
# print(df_stop_corr[df.columns.values[2]][df.columns.values[4]])
# fig = {
#     "data": [

#trace1 = maketrace(df1[newlist[1]], newlist[1], 'negative', 'Short')
#trace2 = maketrace(df2[newlist[1]], newlist[1], 'positive', 'Long')
#trace3 = maketrace(df1[newlist[2]], newlist[2], 'negative', 'Short')
#trace4 = maketrace(df2[newlist[2]], newlist[2], 'positive', 'Long')
# trace5 = maketrace(df[newlist[2]][df['Signal2'] == '通過'], newlist[2], 'negative', 'Pass')
# trace6 = maketrace(df[newlist[2]][df['Signal2'] == '停止'], newlist[2], 'positive', 'Stop')
# trace7 = maketrace(df[newlist[3]][df['Signal2'] == '通過'], newlist[3], 'negative', 'Pass')
# trace8 = maketrace(df[newlist[3]][df['Signal2'] == '停止'], newlist[3], 'positive', 'Stop')
# trace9 = maketrace(df[newlist[4]][df['Signal2'] == '通過'], newlist[4], 'negative', 'Pass')
# trace10 = maketrace(df[newlist[4]][df['Signal2'] == '停止'], newlist[4], 'positive', 'Stop')
# trace11 = maketrace(df[newlist[5]][df['Signal2'] == '通過'], newlist[5], 'negative', 'Pass')
# trace12 = maketrace(df[newlist[5]][df['Signal2'] == '停止'], newlist[5], 'positive', 'Stop')

#fig.append_trace(trace1,1,1)
#fig.append_trace(trace2,1,1)
#fig.append_trace(trace3,1,2)
#fig.append_trace(trace4,1,2)
# fig.append_trace(trace5,1,3)
# fig.append_trace(trace6,1,3)
# fig.append_trace(trace7,1,4)
# fig.append_trace(trace8,1,4)
# fig.append_trace(trace9,1,5)
# fig.append_trace(trace10,1,5)
# fig.append_trace(trace11,1,6)
# fig.append_trace(trace12,1,6)
#     "layout" : {
#        "yaxis": {
#            "zeroline": False,
#        },
#        "violingap": 0,
#        "violinmode": "overlay"
#    }
# }


#offline.plot(fig, filename = 'split1.html', validate = False, image_filename='split', image='svg', image_height=1080, image_width=800)