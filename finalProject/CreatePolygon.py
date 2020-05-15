# -*- coding: utf-8 -*-
"""
Created on 2019/10/2

@author: yhy
用来生成随机的polygon
"""
import random
import rectangleCover
import Class

'''
存在的问题
1.在扩展cell时没有考虑是否可以扩展，即检测一下要扩展的cell是否已经不是hole了
2.没有考虑在扩展是出现死路怎么处理，也就是在指定扩展的步骤内出现死路，但是扩展数量还不够的情况
思路：
建立一个检测函数：
    输入一个cell返回其周边cell的hole情况
    没走一步就做一次检测
在考虑移动时加上一个指标：
目前的指标是，cell所在的位置和其来的方向，加入一个指标检测其周围的cell情况，确定可移动的位置
'''

random.seed(5)
direction={1:'left',2:'up',3:'right',4:'down'}
Cell_neighbor = {'left_extensible':1,'top_extensible':2,'right_extensible':3,'bottom_extensible':4}
Cell_neighbor1 = {1:'left_extensible',2:'top_extensible',3:'right_extensible',4:'bottom_extensible'}


# 功能性function
# 输入a，b代表随机数产生范围
def createRandom(a,b):
    return random.randint(a, b)

# 规定产生的网格都在第一象限内，也就是下边界和左边界分别为x轴，y轴
# 注意xlineList中的元素作为纵坐标，xline指平行于x轴的线的集合
def createXline(XlineRange):
    temp=[]
    for i in range (1,XlineRange):
        temp.append(i)
    # 先设定为选取比最大范围少5根的形式，所以在测试时注意输入不能小于5，稍微取大点
    #注意这里的减5是可以调节的，大于0小于xlineRange就行，为了测试方便，给定一个固定值
    Xline = random.sample(temp, XlineRange - 5)
    Xline.extend([0,XlineRange])
    Xline.sort(reverse=True)
    return Xline

def createYline(YlineRange):
    temp=[]
    for i in range (1, YlineRange):
        temp.append(i)
    # 先设定为选取比最大范围少4根的形式，所以在测试时注意输入不能小于4，稍微取大点
    Yline = random.sample(temp, YlineRange - 5)
    Yline.extend([0, YlineRange])
    Yline.sort()
    return Yline

# 重复代码，在grid类中有类似方法
def createGridC(xline, yline):
    temp = []
    for i in range(len(yline) - 1):
        for j in range(1, len(xline)):
            # 少存一格交点坐标，及最上面的xline和最右边的yline不用计入
            temp.append(Class.Cell(yline[i], xline[j], yline[i+1] - yline[i], xline[j-1] - xline[j]))
    return temp

#根据一个点找到cell在列表中的位置，可以调节根据哪个点寻找
def findCellIndex(point,gridList,whichPoint=1):
    if whichPoint == 1:
        for i in range(0, len(gridList)):
            if gridList[i].point1.coordinate == point:
                return i
    elif whichPoint == 2:
        for i in range(0, len(gridList)):
            if gridList[i].point2.coordinate == point:
                return i
    elif whichPoint == 3:
        for i in range(0, len(gridList)):
            if gridList[i].point3.coordinate == point:
                return i
    elif whichPoint == 4:
        for i in range(0, len(gridList)):
            if gridList[i].point4.coordinate == point:
                return i
    return len(gridList)#这里返回gridList的因为gridList的index最长到gridList-1

# 检测一个点的邻居是否为空
def neighborCheck(cell,gridList,direction):
    temp=0
    # print(direction,len(gridList))
    if direction == 'left':
        temp = findCellIndex(cell.point1.coordinate,gridList,4)
        if temp == len(gridList):
            return 'exist'
        else:
            if gridList[temp].holeNot == 1:
                return 'left_extensible'
            else:
                return 'exist'
    elif direction == 'up':
        temp = findCellIndex(cell.point2.coordinate,gridList)
        if temp == len(gridList):
            return 'hole'
        else:
            if gridList[temp].holeNot == 1:
                return 'top_extensible'
            else:
                return 'exist'
    elif direction == 'right':
        temp = findCellIndex(cell.point4.coordinate,gridList)
        if temp == len(gridList):
            return 'hole'
        else:
            if gridList[temp].holeNot == 1:
                return 'right_extensible'
            else:
                return 'exist'
    elif direction == 'down':
        temp = findCellIndex(cell.point1.coordinate,gridList,2)
        if temp == len(gridList):
            return 'exist'
        else:
            if gridList[temp].holeNot == 1:
                return 'bottom_extensible'
            else:
                return 'exist'


#下面为扩展移动功能

# 开始的cell确定,先暂时随便给一个开始cell
def startCell(xline,yline,gridList):
    x = xline[int((len(xline)/2))]
    y = yline[0]
    return gridList[findCellIndex([y,x],gridList)]

def extendAct(cell,direction,yline,gridList):
    # 向上扩展
    if direction == 'up':
        return gridList[findCellIndex(cell.point1.coordinate, gridList)-1]
    elif direction == 'down':
        return gridList[findCellIndex(cell.point1.coordinate, gridList) + 1]
    elif direction == 'right':
        return gridList[findCellIndex(cell.point1.coordinate, gridList)+(len(yline)-1)]
    elif direction == 'left':
        return gridList[findCellIndex(cell.point1.coordinate, gridList)-(len(yline)-1)]

#定义cell所在的八种状态，在四个角上，和在四条边界上
# 判断是否在grid的边界上，是则返回在哪条边界上
# def CellPosition(Cell, xline, yline):
#     if Cell.point1.coordinate[0] == yline[0]:
#         if Cell.point1.coordinate[1] == xline[-1]:
#             return 'l_edge and bottom'
#         elif Cell.point3.coordinate[1] == xline[0]:
#             return 'l_edge and top'
#         else:
#             return 'l_edge'
#     elif Cell.point4.coordinate[0] == yline[-1]:
#         if Cell.point1.coordinate[1] == xline[-1]:
#             return 'r_edge and bottom'
#         elif Cell.point3.coordinate[1] == xline[0]:
#             return 'r_edge and top'
#         else:
#             return 'r_edge'
#     elif Cell.point1.coordinate[1] == xline[-1]:
#         return 'bottom'
#     elif Cell.point1.coordinate[1] == xline[0]:
#         return 'bottom'

# 输入一个随机数，根据输入返回移动方向
def createDirectionP2(randomNum):
    if randomNum == 1:
        return 'left'
    elif randomNum == 2:
        return 'up'
    elif randomNum == 3:
        return 'right'
    elif randomNum == 4:
        return 'down'

# 根据cell所在的状态确定可以移动的方向，并且随机产生将要移动的方向
# def createDirection(comeDirection,cellPosition):
#     temp=[]
#     for element in list(Cell_comeDir.keys()):
#         if comeDirection == element:
#             temp1=Cell_comeDir[element]
#             break
#     for element in list(Cell_position.keys()):
#         if cellPosition == element:
#             temp2=Cell_position[element]
#             break
#     for element in temp1:
#         if element in temp2:
#             temp.append(element)
#     return createDirectionP2(random.choice(temp))

def createDirectionNew(Cell,gridList):
    temp=[]
    for i in range(1,5):
        # print(neighborCheck(Cell, gridList, direction[i]),direction[i],'+++++')
        if Cell_neighbor1[i] == neighborCheck(Cell, gridList, direction[i]):#direction是全局变量字典
            temp.append(i)
        else:
            continue
    if len(temp)==0:#防止temp是空数组
        return
    else:
        return createDirectionP2(random.choice(temp))



#
def extendCell(startCell,gridList,yline,extendNum):
    if extendNum != 0:
        extendNum = extendNum-1
        startCell.holeNot=0
        # #随机生成一个要走的方向
        direction = createDirectionNew(startCell, gridList)
        NextCell = extendAct(startCell,direction,yline,gridList)#在这个方向想移动扩展cell
        if NextCell == None:#为了防止NextCell不是空指针
            return
        else:
            return extendCell(NextCell, gridList, yline,extendNum)
    else:
        return


# 测试

temp1= createXline(10)
temp2 = createYline(10)
temp_grid = createGridC(temp1,temp2)
tempStartCell=startCell(temp1,temp2,temp_grid)
# print(temp1,temp2,tempStartCell.point1.coordinate)
extendCell(tempStartCell,temp_grid ,temp2,7)

count=0
for element in temp_grid:
    print(element.holeNot,count)
    count = count + 1