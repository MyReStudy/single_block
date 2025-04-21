import pandas as pd


# class PickingState:
#     def __init__(self, id):
#         self.id = id
#         # self.decision = []
#         self.upFlag = 0
#         self.downFlag = 0
#         self.middleFlag = 0
#         self.routeNum = 0
#
#     def getId(self):
#         return self.id
#
#     def isOneRoute(self):
#         flag = self.upFlag + self.downFlag + self.middleFlag
#         if (flag == 3 or flag == 1):
#             self.routeNum = 1
#             return True
#         else:
#             self.routeNum = 2
#             return False
def getAisleList(warehouseInformation):  # 所有存着货物的列 按照从小到大顺序排列
    aislelist = sorted(warehouseInformation['aisle'].unique())
    return aislelist

def initResult(aisleNum):
    columns1 = [i for i in aisleNum]
    index1 = ['state1', 'state2', 'state3', 'state4_1', 'state4_2']
    initResult = pd.DataFrame(columns=columns1, index=index1)
    return initResult

#State是所有可以变为这个状态的方法 其中state4_1表示一条路的state4 这说明前面已经是一条路了
#其中 除了state4 其他状态前面必然是一条路
State = {
    'state1': [['state1', 2], ['state1', 3], ['state1', 4], ['state2', 1], ['state3', 1], ['state4_1', 1], ['state4_2', 1]], #7  2 2 3 1 1 2 2  13
    'state2': [['state1', 1], ['state2', 2], ['state4_1', 3], ['state4_1', 4]], #4  1 1 3 3  8
    'state3': [['state1', 1], ['state3', 3], ['state4_1', 2], ['state4_1', 4]], #4  1 1 3 3  8
    'state4_1': [['state1', 1], ['state4_1', 2],['state4_1', 3],['state4_1', 4]],  # 4   1 3 3 3  10
    'state4_2': [['state2', 3], ['state2', 4], ['state3', 4], ['state3', 2], ['state4_2', 2], ['state4_2', 3], ['state4_2', 4]] #7   3 3 3 3 3 3  18
}

# StateAndconfigs = {
#     'state1' : [1,2,3,4],
#     'state2' : [1,2,3,4],
#     'state3' : [1,2,3,4],
#     'state4_1' : [1,2,3,4],
#     'state4_2' : [2,3,4]
#
# }

initAndLastState = {
    'state1': 1,
    'state2': 2,
    'state3': 3,
    'state4_1': 4,
    'state4_2': 4
}

# def getOneRouteFlag(method,state,preflag):#左边和中间的配置、右边的状态、左边之前成一条路了不
#     #flag=0永远会是一条路了不用管了; flag=1目前是一条路可能会变成两条路; flag=2是两条路
#     preState=method[0]
#     vertical=method[1]
#     newState=state
#     nowflag=-1
#     if preflag == 1:
#         nowflag=1
#     elif preflag == 2:
#         if vertical==1:
#             nowflag=1
#         else:
#             nowflag=2
#     elif preflag == 0:
#         if vertical==1:
#             nowflag=1
#         elif newState=='state4':
#             nowflag=2
#     return nowflag

# def getInitFlag(state):
#     if state=='state1':
#         return 1
#     elif state=='state2' or state=='state3':
#         return 0
#     else:
#         return 2
#
# def getFinalFlag(preflag,vertical):
#     if preflag==1:
#         return 1
#     elif preflag==0:
#         return 1
#     else:
#         if vertical==1:
#             return 1
#         else:
#             return 2


if __name__ == '__main__':
    initResult(6)