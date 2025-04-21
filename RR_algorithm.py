import math
from math import nan

import numpy as np
import pandas as pd
import time

pd.set_option('display.max_columns', None)
pd.set_option('expand_frame_repr', False)


class RRPicking:

    def __init__(self, distanceMatrixPath, negativeToPositivePath, positiveToNegativePath,
                 warehouseInformation):
        self.distanceMatrix = pd.read_excel(distanceMatrixPath, index_col=0)
        self.negativeToPositive = pd.read_excel(negativeToPositivePath, index_col=0)
        self.positiveToNegative = pd.read_excel(positiveToNegativePath, index_col=0)
        self.warehouseInformation = pd.read_excel(warehouseInformation, index_col=0)
        self.aisleNum = self.warehouseInformation.loc[:, "aisle"].max()  # 删去了右边的空巷道 但是中间如果有空的还需要判断
        self.resultTable = self.formResultTable()
        self.resultDistance = self.formResultTable()
        self.calNum = 0
        self.startTime=0.0
        self.endTime = 0.0
        self.finalResult=0
        self.totalTime=0.0

    def formResultTable(self):
        '''
        :return: 初始结果表
        '''
        if math.isnan(self.aisleNum):
            return
        equivalenceClass = ['U,U,1C', 'E,0,1C', '0,E,1C', 'E,E,1C', 'E,E,2C', '0,0,0C', '0,0,1C']
        state = []
        for i in range(1, self.aisleNum + 1):
            for j in ['-', '+']:
                temp = str(i) + j
                state.append('L' + temp)
        resultTable = pd.DataFrame(
            columns=state,  # 指定列属性
            index=equivalenceClass  # 指定行索引
        )
        return resultTable

    def calculationVertical(self, aisle):  # 竖向的配置 即从-变成+ 计算每个配置下的距离
        '''
        :param configuration: 决策
        :param distance: 之前的距离
        :param aisle: 阶段中的巷道
        :return: 当前决策的距离
        '''
        lengthForVer = {}
        cofList=[1,2,3,4,5,6]
        for configuration in cofList:
            if configuration == 1:
                self.calNum = self.calNum
                lengthForVer[configuration] = self.distanceMatrix['a{}'.format(aisle)]['b{}'.format(aisle)]
            elif configuration == 2:
                vertexContainedInAisle = self.warehouseInformation[self.warehouseInformation.aisle == aisle].index.tolist()
                if (len(vertexContainedInAisle) == 0):
                    lengthForVer[configuration] = None
                else:
                    self.calNum = self.calNum + 1
                    distanceInAisle = []
                    for vertex in vertexContainedInAisle:
                        distanceInAisle.append(self.distanceMatrix['a{}'.format(aisle)][vertex])
                    maxIndex = distanceInAisle.index(max(distanceInAisle))
                    maxDistance = self.distanceMatrix['a{}'.format(aisle)][vertexContainedInAisle[maxIndex]]
                    lengthForVer[configuration] = maxDistance * 2
            elif configuration == 3:
                vertexContainedInAisle = self.warehouseInformation[self.warehouseInformation.aisle == aisle].index.tolist()
                if (len(vertexContainedInAisle) == 0):
                    # return 999999
                    lengthForVer[configuration] = None
                else:
                    self.calNum = self.calNum + 1
                    distanceInAisle = []
                    for vertex in vertexContainedInAisle:
                        distanceInAisle.append(self.distanceMatrix['b{}'.format(aisle)][vertex])
                    maxIndex = distanceInAisle.index(max(distanceInAisle))
                    maxDistance = self.distanceMatrix['b{}'.format(aisle)][vertexContainedInAisle[maxIndex]]
                    lengthForVer[configuration] = maxDistance * 2
            elif configuration == 4:
                vertexContainedInAisle = self.warehouseInformation[self.warehouseInformation.aisle == aisle].index.tolist()
                if (len(vertexContainedInAisle) <= 1):
                    lengthForVer[configuration] = None
                else:
                    self.calNum = self.calNum + 3
                    maximumSpac = 0
                    distanceFromA = dict.fromkeys(vertexContainedInAisle)
                    vertex_i = ''
                    vertex_j = ''
                    for v in vertexContainedInAisle:
                        distanceFromA[v] = self.distanceMatrix.loc['a{}'.format(aisle)][v]
                    distanceFromASorted = sorted(distanceFromA.items(), key=lambda x: x[1], reverse=False)
                    vertexSortedList = []
                    for temp in distanceFromASorted:
                        vertexSortedList.append(temp[0])
                    # vertexSortedList = 1
                    for vertex1 in vertexContainedInAisle:
                        for vertex2 in vertexContainedInAisle:
                            if (self.distanceMatrix[vertex1][vertex2] >= maximumSpac): #7月 在这里加了等于号
                                if (abs(int(vertexSortedList.index(vertex1)) - int(vertexSortedList.index(vertex2))) == 1):
                                    # if(abs(int(vertex1[-1])-int(vertex2[-1]))==1):#保证相邻
                                    maximumSpac = self.distanceMatrix[vertex1][vertex2]
                                    vertex_i = vertex1
                                    vertex_j = vertex2
                    if (self.distanceMatrix['a{}'.format(aisle)][vertex_i] <= self.distanceMatrix['a{}'.format(aisle)][vertex_j]):
                        topVertex = vertex_i
                        downVertex = vertex_j
                    else:
                        topVertex = vertex_j
                        downVertex = vertex_i
                    distanceInAisle = self.distanceMatrix['a{}'.format(aisle)][topVertex] * 2 + \
                                      self.distanceMatrix['b{}'.format(aisle)][downVertex] * 2
                    lengthForVer[configuration] = distanceInAisle
            elif configuration == 5:
                self.calNum = self.calNum + 1
                lengthForVer[configuration] = self.distanceMatrix['a{}'.format(aisle)]['b{}'.format(aisle)] * 2
            elif configuration == 6:  # this is not a feasible configuration if there is any item to picked in aisle j
                vertexContainedInAisle = self.warehouseInformation[self.warehouseInformation.aisle == aisle].index.tolist()
                if (len(vertexContainedInAisle) != 0):
                    lengthForVer[configuration] = None
                # self.calNum = self.calNum + 1
                else:
                    lengthForVer[configuration] = 0
        return lengthForVer
        # else:
        #     return 999999

    def calculatedHorizontal(self, aisle):  # 水平 计算每个配置下的距离
        lengthForHor = {}
        cofList=[1,2,3,4,5]
        for configuration in cofList:
            # if configuration == 5:
            #     return distance + 0
            if configuration == 1:
                self.calNum = self.calNum + 1
                lengthForHor[configuration] = self.distanceMatrix['a{}'.format(aisle)]['a{}'.format(int(aisle) - 1)] + \
                       self.distanceMatrix['b{}'.format(aisle)]['b{}'.format(int(aisle) - 1)]
            if configuration == 2:
                self.calNum = self.calNum + 1
                lengthForHor[configuration] = self.distanceMatrix['a{}'.format(aisle)]['a{}'.format(int(aisle) - 1)] * 2
            if configuration == 3:
                self.calNum = self.calNum + 1
                lengthForHor[configuration] = self.distanceMatrix['b{}'.format(aisle)]['b{}'.format(int(aisle) - 1)] * 2
            elif configuration == 4:
                self.calNum = self.calNum + 3
                lengthForHor[configuration] = self.distanceMatrix['a{}'.format(aisle)]['a{}'.format(int(aisle) - 1)] * 2 + \
                       self.distanceMatrix['b{}'.format(aisle)]['b{}'.format(int(aisle) - 1)] * 2
            elif configuration == 5: #有歧义
                lengthForHor[configuration] = 0
        return lengthForHor

    def getNegativeToPositiveDict(self):
        # 由负到正 各种等价类可以由谁变过去
        stateChangeDict = {}
        rowList = list(self.resultTable.index.values)  # 行索引的列表
        for tempState in rowList:  # 遍历(下一步)的每一个步骤
            possiblePreviousState = []  # 可以变成当前状态的上一个状态列表
            for indexs in self.negativeToPositive.index:  # 行
                # for i in range(len(self.negativeToPositive.loc[indexs].values)):  # 列
                for i in range(len(self.negativeToPositive.loc[indexs].values)):  # 列
                    if (self.negativeToPositive.loc[indexs].values[i] == tempState):  # 当前状态对应的行列索引
                        possiblePreviousState.append([indexs, i + 1])  # 当前状态可能的前一个状态所对应的行索引和列索引集合
                        # print(self.negativeToPositive.loc[indexs].values[i])
            stateChangeDict[tempState] = possiblePreviousState
        return stateChangeDict

    def getPositiveToNegativeDict(self):
        # 由正到负
        stateChangeDict = {}
        rowList = list(self.resultTable.index.values)  # 行索引的列表
        for tempState in rowList:  # 遍历(下一步)的每一个步骤
            possiblePreviousState = []  # 可以变成当前状态的上一个状态列表
            for indexs in self.positiveToNegative.index:  # 行
                # for i in range(len(self.negativeToPositive.loc[indexs].values)):  # 列
                for i in range(len(self.positiveToNegative.loc[indexs].values)):  # 列
                    if (self.positiveToNegative.loc[indexs].values[i] == tempState):  # 当前状态对应的行列索引
                        possiblePreviousState.append([indexs, i + 1])  # 当前状态可能的前一个状态所对应的行索引和列索引集合
                        # print(self.negativeToPositive.loc[indexs].values[i])
            stateChangeDict[tempState] = possiblePreviousState
        return stateChangeDict

    def formingPath(self):
        '''
        预处理
        1、初始化结果表
        2、取出所有的变换方式 以字典形式存储
        {
        下一阶段的状态:[[],[],[]]
        }
        '''
        if math.isnan(self.aisleNum):
            print('没有待拣货物!')
            return
        # self.resultTable['L1-'] = [None] * 7
        # self.resultDistance['L1-'] = [None] * 7
        # self.resultDistance.loc['0,0,0C', 'L1-'] = 0

        columnNameList = list(self.resultTable.index.values)  # 取出来所有的等价类
        negativeToPositiveDict = self.getNegativeToPositiveDict()
        positiveToNegativeDict = self.getPositiveToNegativeDict()
        resultDistanceTemp = self.resultDistance.copy()

        lengthForVer = self.calculationVertical(1)
        resultDistanceTemp.loc['U,U,1C', 'L1+']=lengthForVer[1]
        resultDistanceTemp.loc['E,0,1C', 'L1+'] = lengthForVer[2]
        resultDistanceTemp.loc['0,E,1C', 'L1+'] = lengthForVer[3]
        resultDistanceTemp.loc['E,E,2C', 'L1+'] = lengthForVer[4]
        resultDistanceTemp.loc['E,E,1C', 'L1+'] = None
        resultDistanceTemp.loc['0,0,0C', 'L1+'] = None
        resultDistanceTemp.loc['0,0,1C', 'L1+'] = None
        self.resultTable.loc['U,U,1C', 'L1+']=1
        self.resultTable.loc['E,0,1C', 'L1+']=2
        self.resultTable.loc['0,E,1C', 'L1+']=3
        self.resultTable.loc['E,E,2C', 'L1+']=4
        # self.resultTable
        # self.resultTable
        # self.resultTable=resultDistanceTemp

        # a=self.aisleNum
        preState = '+'  # 设置上一次的状态
        currentAisle = 1

        while (not (preState == '+' and currentAisle == self.aisleNum)): #如果上一个状态是- 且当前的通道不是最后一个
            if preState == '-':  # 如果上一个状态是- 那么下一个状态不用改变过道号 但是状态要变成+
                currentState = '+'  # 改变状态
                columnName = 'L' + str(currentAisle) + currentState  # 当前的列+状态
                lengthForVer = self.calculationVertical(currentAisle)
                for equivalenceClass in columnNameList:  # 对于每一个等价类找最短距离
                    configurationMethodList = negativeToPositiveDict[equivalenceClass]  # 可以变成该等价类的方法(上一个等价类+配置)列表
                    # minDist = 99999
                    distList=[]
                    # minPreClass = ''
                    # methodList = []
                    for methodIdx in range(len(configurationMethodList)):  # 对可以变成该等价类的方法进行遍历
                        preEquivalenceClass = configurationMethodList[methodIdx][0]  # 上一个等价类
                        preDist = resultDistanceTemp.loc[preEquivalenceClass]['L' + str(currentAisle) + '-']  # 之前的距离
                        #建立一个列表，从这里面选出来最小的元素，如果列表为空，这个位置写-
                        if preDist is None:
                            distList.append(None)
                        else:
                            if lengthForVer[configurationMethodList[methodIdx][1]] is not None:
                                currentDist = preDist+lengthForVer[configurationMethodList[methodIdx][1]]
                                self.calNum = self.calNum + 1
                                    # self.calculationVertical \
                                    # (configurationMethodList[methodIdx][1], preDist, currentAisle)  # 配置 之前的距离 当前aisle-->当前距离
                                distList.append(currentDist)
                        # methodList.append(configurationMethodList[methodIdx][1])
                    distanceContainingOnlyNumbers=list(filter(None, distList))
                    if not distanceContainingOnlyNumbers:
                        resultDistanceTemp.loc[equivalenceClass, columnName] = None
                    else:
                        minDist=min(distanceContainingOnlyNumbers)
                        resultDistanceTemp.loc[equivalenceClass, columnName] = minDist
                        self.resultTable.loc[equivalenceClass, columnName] = '{},{},{}'.format(minDist,
                                                                                               configurationMethodList[distList.index(minDist)][0],
                                                                                               configurationMethodList[distList.index(minDist)][1])
                    preState = '+'  # 计算结束 上一个状态更新为 +

            else:
                currentState = '-'  # 如果上一个状态是+ 那么下一个状态要改变过道号 同时状态变成-
                currentAisle = currentAisle + 1
                columnName = 'L' + str(currentAisle) + currentState
                lengthForHor = self.calculatedHorizontal(currentAisle)
                for equivalenceClass in columnNameList:
                    configurationMethodList = positiveToNegativeDict[equivalenceClass]
                    distList = []
                    for methodIdx in range(len(configurationMethodList)):
                        preEquivalenceClass = configurationMethodList[methodIdx][0]
                        preDist = resultDistanceTemp.loc[preEquivalenceClass]['L' + str(currentAisle - 1) + '+']
                        if preDist is None:
                            distList.append(None)
                        else:
                            if lengthForHor[configurationMethodList[methodIdx][1]] is not None:
                                currentDist = preDist+lengthForHor[configurationMethodList[methodIdx][1]]
                                self.calNum=self.calNum+1
                                    # self.calculatedHorizontal \
                                    # (configurationMethodList[methodIdx][1], preDist, currentAisle)
                                distList.append(currentDist)
                        # methodList.append(configurationMethodList[methodIdx][1])
                    distanceContainingOnlyNumbers=list(filter(None, distList))
                    if not distanceContainingOnlyNumbers:
                        resultDistanceTemp.loc[equivalenceClass, columnName] = None
                        self.resultTable.loc[equivalenceClass, columnName] = None
                    else:
                        minDist = min(distanceContainingOnlyNumbers)
                        resultDistanceTemp.loc[equivalenceClass, columnName] = minDist
                        self.resultTable.loc[equivalenceClass, columnName] = '{},{},{}'.format(minDist,
                                                                                           configurationMethodList[distList.index(minDist)][0],
                                                                                           configurationMethodList[distList.index(minDist)][1])
                    preState = '-'
        self.resultDistance = resultDistanceTemp

    def start(self):
        self.startTime = time.perf_counter()

    def end(self):
        self.endTime = time.perf_counter()
        self.totalTime = self.endTime - self.startTime



if __name__ == "__main__":

    total_time= []
    result_total = []
    negativeToPositivePath = 'Table1.xlsx'
    positiveToNegativePath = 'Table2.xlsx'

    for ii in range(1,21):
        time_tmp = []
        for jj in range(1,101):
            distanceMatrixPath = f'data/{ii}/测试数据{jj}/距离矩阵.xlsx'
            warehouseInformation = f'data/{ii}/测试数据{jj}/仓库信息.xlsx'
            time_start = time.perf_counter()
            picking = RRPicking(distanceMatrixPath, negativeToPositivePath, positiveToNegativePath, warehouseInformation)
            picking.formingPath()
            if not math.isnan(picking.aisleNum):
                # print(picking.resultTable)  # 待解开注释
                result = picking.resultTable.iloc[:, -1]
                resultClassList = ['E,0,1C', '0,E,1C', 'E,E,1C']
                result = result.drop(index=['U,U,1C', 'E,E,2C', '0,0,0C', '0,0,1C']).tolist()
                temp = []
                if ii == 1:
                    result = picking.resultDistance.iloc[:, -1]
                    result = result.drop(index=['U,U,1C', 'E,E,2C', '0,0,0C', '0,0,1C']).tolist()
                    if 0 in result:
                        result = list(filter(None, result))
                        result.append(0)
                    else:
                        result = list(filter(None, result))
                    temp.append(min(result))
                else:
                    for i in result:
                        temp.append(float(i.split(',')[0]))
                idx = temp.index(min(temp))
                result_total.append(temp[idx])
                time_end = time.perf_counter()
                time_sum = time_end - time_start
                time_tmp.append(time_sum)
        total_time.append(np.mean(time_tmp))

    # 创建一个DataFrame，列表作为列
    df_time = pd.DataFrame({'Column1': total_time})
    # 保存为Excel文件
    df_time.to_excel('RR-time.xlsx', index=False)  # index=False表示不保存行索引

    df_result = pd.DataFrame({'Column2': result_total})
    df_result.to_excel('RR-result.xlsx', index=False)  # index=False表示不保存行索引