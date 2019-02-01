import numpy as np
import json
import pprint
import pandas as pd
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
import seaborn as sns
import math

def executeHierarchicalClustering(data, graph=False, d=True):
    if(graph and d):
        sns.distplot(data)
        plt.show()

    #階層クラスタリング
    result1 = linkage(data, 
                    metric = 'euclidean', 
                    method = 'ward')

    print(result1[:, 2])

    #閾値設定
    threshold = 0.7 * np.max(result1[:, 2])
    #threshold = result1[result1.shape[0] - 2, 2]
    #threshold1 = result1[result1.shape[0] - 3, 2]
    #threshold2 = result1[result1.shape[0] - 4, 2]


    #クラスタリング結果（インデックス）取得
    clustered = fcluster(result1, threshold, criterion='distance')
    #分類したクラスタ数
    m=np.max(clustered)
    print(clustered)
    clusterindex = np.array([])


    if(graph):
        #ヒストグラム作成用
        if(d):
            x=[]
            for i in range(np.max(clustered)):
                clustereddata = data.values.flatten()[np.where(clustered == i+1)]
                x.append(clustereddata)

            print(x)
            #ヒストグラム描画
        
            plt.hist(x=x, bins=20)
            plt.show()
        else:
            fig = plt.figure()

            ax = fig.add_subplot(1,1,1)
            for i in range(np.max(clustered)):
                x=data[data.columns.values[0]].values.flatten()[np.where(clustered == i+1)]
                y=data[data.columns.values[1]].values.flatten()[np.where(clustered == i+1)]
                ax.scatter(x,y)

            ax.set_xlabel('x')
            ax.set_ylabel('y')
            plt.show()
            


        #デンドログラム描画
        dendrogram(result1, color_threshold=threshold)
        plt.title("Dedrogram")
        plt.ylabel("Threshold")
        plt.show()

    #元データにクラスタリング結果を追加
    data['Cluster'] = clustered

    return data, m

def getCorrelation(result1, m1, result2, m2):
    sum = 0
    for t in range(m1):
        concat = pd.concat([result1, result2], axis=1)

        col = concat.columns.values
        col[1] = 'cluster1'
        col[3] = 'cluster2'
        concat.columns = col

        matrix = np.array([])
        for i in range(m2) :
            selectedData = concat[concat[concat.columns.values[1]] == t+1]
            selectedData = selectedData[selectedData[selectedData.columns.values[3]] == i+1]

            count = len(selectedData)

            matrix = np.append(matrix, count)
        if(len(concat[concat[concat.columns.values[1]] == t+1] != 0)):
            matrix = matrix / len(concat[concat[concat.columns.values[1]] == t+1])
            print(matrix)
            for item in matrix:
                sum += -item * math.log(item)
                print(sum)

    for t in range(m2):
        concat = pd.concat([result1, result2], axis=1)

        col = concat.columns.values
        col[1] = 'cluster1'
        col[3] = 'cluster2'
        concat.columns = col

        matrix = np.array([])
        for i in range(m1) :
            selectedData = concat[concat[concat.columns.values[3]] == t+1]
            selectedData = selectedData[selectedData[selectedData.columns.values[1]] == i+1]

            count = len(selectedData)

            matrix = np.append(matrix, count)
        if(len(concat[concat[concat.columns.values[3]] == t+1] != 0)):
            matrix = matrix / len(concat[concat[concat.columns.values[3]] == t+1])
            for item in matrix:
                sum += -item * math.log(item)
                print(sum)

    correlation = math.exp(-sum)
    return correlation

#JSONデータ読み込み
with open('pcpdata17.json', encoding='utf-8') as f:
    d = json.load(f)
    data = json.dumps(d, ensure_ascii=False)
    df = pd.read_json(data)


#Column Name
newlist = [df.columns.values[0],df.columns.values[1],df.columns.values[2],df.columns.values[3]
,df.columns.values[6],df.columns.values[7]]

print(newlist)

Result = []
M = []

for i in range(4):
    r, m = executeHierarchicalClustering(df.iloc[:, i:i+1])
    Result.append(r)
    M.append(m)

for i in range(6,8):
    r, m = executeHierarchicalClustering(df.iloc[:, i:i+1])
    Result.append(r)
    M.append(m)

print(M)


#ResultTime,Timem = executeHierarchicalClustering(df.iloc[:, 0:1])
#ResultEnergy, Energym = executeHierarchicalClustering(df.iloc[:, 1:2])
#ResultNextTime, NextTimem = executeHierarchicalClustering(df.iloc[:, 2:3])
#ResultNextEnergy, NextEnergym = executeHierarchicalClustering(df.iloc[:, 3:4])
#ResultSumTime, SumTimem = executeHierarchicalClustering(df.iloc[:, 6:7])
#ResultSumLost, SumLostm = executeHierarchicalClustering(df.iloc[:, 7:8])

#Result2d, m2d = executeHierarchicalClustering(df.iloc[:, 0:2], False, False)
#ResultNext, Nextm = executeHierarchicalClustering(df.iloc[:, 2:4], False, False)
#ResultSum, Summ = executeHierarchicalClustering(df.iloc[:, 6:8], False, False)


correlationMatrix = []
for t in range(4):
    list = []
    for i in range(4):
        if(i == t):
            list.append(0)
        else:    
            correlation = getCorrelation(Result[t], M[t], Result[i], M[i])
            list.append(correlation)

    correlationMatrix.append(list)


print(correlationMatrix)

sns.heatmap(correlationMatrix, cmap='bwr')
plt.show()


Result = []
M = []

for i in range(0,4,2):
    r, m = executeHierarchicalClustering(df.iloc[:, i:i+2], False, False)
    Result.append(r)
    M.append(m)
    print(r)
    print(m)


r, m = executeHierarchicalClustering(df.iloc[:, 6:8], True, False)
Result.append(r)
M.append(m)
print(r)
print(m)



#ResultTime,Timem = executeHierarchicalClustering(df.iloc[:, 0:1])
#ResultEnergy, Energym = executeHierarchicalClustering(df.iloc[:, 1:2])
#ResultNextTime, NextTimem = executeHierarchicalClustering(df.iloc[:, 2:3])
#ResultNextEnergy, NextEnergym = executeHierarchicalClustering(df.iloc[:, 3:4])
#ResultSumTime, SumTimem = executeHierarchicalClustering(df.iloc[:, 6:7])
#ResultSumLost, SumLostm = executeHierarchicalClustering(df.iloc[:, 7:8])

#Result2d, m2d = executeHierarchicalClustering(df.iloc[:, 0:2], False, False)
#ResultNext, Nextm = executeHierarchicalClustering(df.iloc[:, 2:4], False, False)
#ResultSum, Summ = executeHierarchicalClustering(df.iloc[:, 6:8], False, False)


correlationMatrix = []
for t in range(3):
    list = []
    for i in range(3):
        if(i == t):
            list.append(0)
        else:    
            correlation = getCorrelation(Result[t], M[t], Result[i], M[i])
            list.append(correlation)

    correlationMatrix.append(list)


#print(correlationMatrix)

sns.heatmap(correlationMatrix, cmap='bwr')
plt.show()