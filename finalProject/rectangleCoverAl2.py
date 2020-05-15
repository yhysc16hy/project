# -*- coding: utf-8 -*-
"""
Created on 2020/3/5

@author: yhy

"""
from math import sqrt
import matplotlib.pyplot as plt
from descartes import PolygonPatch
from matplotlib.pyplot import MultipleLocator
from shapely.geometry import Polygon

import rectangleCover
# import test as TESTset
import Point

direction={1:'left',2:'up',3:'right',4:'down'}

'''
给segment线段添加属性，和x轴的夹角，并且规定垂直于x轴的线段为vertical

对于vertical的线段进行水平平移，否则进行垂直平移

如何判断在哪个方向上进行平移：
    目前设想：
    检测线段的规定的一个方向上的cell是否为hole
    是则在其相反方向，否则就在该方向上进行平移

寻找最大矩形的过程：
    类似之前算法，平移一格，检测平移后的线段是否含有其他顶点，无则继续
    直到有为止
    记录找到的矩形，存放在list中
2020.3.9
先检查一下新的画图方法能不能成功

然后排除问题
    
'''
#算法实现

#####################################
#第一部分，在convex side 边上做最大内接矩形
#####################################

# 检测一条side的规定方向上的一个cell是否为hole，比如检测右侧第一个cell
# 1就代表向右或者向下，0代表向左或向上，在根据slope判断 具体方向
# def checkCellBesideOfSide(side,grid):
#     for element in grid.gridCellL:
#         if element.holeNot == 0 and side.point1.PointsEqualOrNot(element.point2):
#             return 1
#         elif element.holeNot == 0 and side.point2.PointsEqualOrNot(element.point2):
#             return 1
#     return 0

# 检测一条side的规定方向上的一个cell是否为hole，比如检测右侧第一个cell
# 1就代表向右或者向下，0代表向左或向上，在根据slope判断 具体方向
def checkCellBesideOfSide(side,grid):
    count=0
    if side.verticeOrNot == 1:
        # 在线段右侧0.5的位置找一个点
        x = side.point1.coordinate[0]+0.5
        y = (side.point1.coordinate[1]+side.point2.coordinate[1])/2
        segment1=grid.createSegmentVertical(Point.Point(x,y), grid.xlineList[0])#这里生成一条竖线
        for element in grid.segmentList:
            if grid.intersectOrNot(segment1, element):
                count = count + 1
        if (count % 2) == 0:
            return 1
        else:
            return 0
    else:
        # 在线段上方0.5的位置找一个点
        x = (side.point1.coordinate[0] + side.point2.coordinate[0]) / 2
        y = side.point1.coordinate[1]+0.5
        segment1 = grid.createSegment(Point.Point(x, y), grid.ylineList[-1])#这里生成一条横线
        for element in grid.segmentList:
            if grid.intersectOrNot(segment1, element):
                count = count + 1
        if (count % 2) == 0:
            return 1
        else:
            return 0


# 判断segment(side)寻找最大矩形的方向
# 1向左，2向上，3向右，4向下
def findDir(side,grid):
    if side.verticeOrNot == 1:
        if checkCellBesideOfSide(side,grid)==1:
            return 1
        else:
            return 3
    else:
        if checkCellBesideOfSide(side, grid) == 1:
            return 4
        else:
            return 2



# 移动边来寻找矩形，每次调用这个function即为移动一步
def MoveSide(side,grid,direction):
    temp_x1=0
    temp_y1=0
    temp_x2=0
    temp_y2=0
    if direction == 1:
        temp_x1 = side.point1.coordinate[0] - 1
        temp_y1 = side.point1.coordinate[1]
        temp_x2 = side.point2.coordinate[0] - 1
        temp_y2 = side.point2.coordinate[1]
    elif direction == 2:
        temp_x1 = side.point1.coordinate[0]
        temp_y1 = side.point1.coordinate[1] + 1
        temp_x2 = side.point2.coordinate[0]
        temp_y2 = side.point2.coordinate[1] + 1
    elif direction == 3:
        temp_x1 = side.point1.coordinate[0] + 1
        temp_y1 = side.point1.coordinate[1]
        temp_x2 = side.point2.coordinate[0] + 1
        temp_y2 = side.point2.coordinate[1]
    elif direction == 4:
        temp_x1 = side.point1.coordinate[0]
        temp_y1 = side.point1.coordinate[1] - 1
        temp_x2 = side.point2.coordinate[0]
        temp_y2 = side.point2.coordinate[1] - 1
    return Point.Segment(Point.Point(temp_x1,temp_y1),Point.Point(temp_x2,temp_y2))


# 判断一条side是否可以继续移动或者停下来
def CheckSegment(side,grid):
    for element in grid.segmentList:
        if element.verticeOrNot == side.verticeOrNot == 1:#更为准确是，这里应该对比斜率
            if TwoSegOverlapNot(element,side,0) == 1:
                return 1
        elif element.verticeOrNot == side.verticeOrNot == 0:
            if TwoSegOverlapNot(element,side,1) == 1:
                return 1
        else:
            continue
    return 0

#判断两条斜率相同的线段，是否有重叠区域,重点是判断side1是否和side2重叠
#存在问题，有可能该函数参数位置改变，结果不同

# side2为移动的side,side1为要被判断的side,该方法有一个前提就是，前提斜率一样
def TwoSegOverlapNot(side1,side2,x):
    if side1.point1.coordinate[x] != side2.point1.coordinate[x]:
        return 0
    else:
        if x == 1:
            x = 0
        elif x == 0:
            x = 1

        if side2.length>side1.length:
            if (side1.point1.coordinate[x] < side2.point1.coordinate[x] and side1.point1.coordinate[x] >side2.point2.coordinate[x] or
                    side1.point2.coordinate[x] < side2.point1.coordinate[x] and side1.point2.coordinate[x] >side2.point2.coordinate[x]):
                    return 1
        elif side2.length < side1.length:
            if (side2.point1.coordinate[x] < side1.point1.coordinate[x] and side2.point1.coordinate[x] >side1.point2.coordinate[x] or
                    side2.point2.coordinate[x] < side1.point1.coordinate[x] and side2.point2.coordinate[x] >side1.point2.coordinate[x]):
                    return 1
        elif side2.length == side1.length:
            if (side1.point1.coordinate[x] < side2.point1.coordinate[x] and side1.point1.coordinate[x] >side2.point2.coordinate[x] or
                    side1.point2.coordinate[x] < side2.point1.coordinate[0] and side1.point2.coordinate[x] >side2.point2.coordinate[x]):
                    return 1
            elif (side1.point1.PointsEqualOrNot(side2.point1) and side1.point2.PointsEqualOrNot(side2.point2)):
                return 1
        return 0


# 寻找一条convexside的最大矩形
def findMaxRecOfSide(side,grid,direction):
    temp_side = MoveSide(side,grid,direction)
    temp = CheckSegment(temp_side, grid)
    if temp == 1:
        return temp_side
    else:
        return findMaxRecOfSide(temp_side,grid,direction)

# 寻找一个grid中所有的convexside的最大内接矩形
def findMaxRecOfConvexSegInGrid(grid):
    rectangleList = []
    i=0
    for element in grid.convexSegmentL:
        dir=findDir(element, grid)
        # print(dir,'---------',i)
        rectangleList.append(Point.Rectangle(element,findMaxRecOfSide(element,grid,dir)))
        i=i+1
    return rectangleList

#####################################
#第二部分，寻找没有cover的concaveSide
#####################################
# 判断两条list中，其中一条是否完全被另一条覆盖,cover返回1，未cover返回0
def AsideCoveredOrNot(side,concaveSide):
    if side.verticeOrNot == concaveSide.verticeOrNot:
        x = abs(concaveSide.verticeOrNot - 1)
        if side.point1.coordinate[x] != concaveSide.point1.coordinate[x]:
            return 0
        else:
            x = abs(x - 1)
            # 进行分类讨论
            if concaveSide.length > side.length:
                return 0
            elif concaveSide.length < side.length:
                if (concaveSide.point1.coordinate[x] <= side.point1.coordinate[x] and concaveSide.point2.coordinate[x] >= side.point2.coordinate[x]):
                    return 1
            elif concaveSide.length == side.length:
                if (concaveSide.point1.PointsEqualOrNot(side.point1) and concaveSide.point2.PointsEqualOrNot(side.point2)):
                    return 1
            return 0
    else:
        return 0

def findUncoverConcaveSide(grid,rectangleList):
    uncoveredSide=grid.concaveSegmentL
    i = 0 #用来控制位置
    while i < len(uncoveredSide):
        temp = uncoveredSide[i]
        for item in rectangleList:
            if AsideCoveredOrNot(item.leftSegment, uncoveredSide[i]) == 1:
                uncoveredSide.pop(i)
                i = i - 1
                break
            elif AsideCoveredOrNot(item.rightSegment, uncoveredSide[i]) == 1:
                uncoveredSide.pop(i)
                i = i - 1
                break
            elif AsideCoveredOrNot(item.SegmentL1R1, uncoveredSide[i]) == 1:
                uncoveredSide.pop(i)
                i = i - 1
                break
            elif AsideCoveredOrNot(item.SegmentL2R2, uncoveredSide[i]) == 1:
                uncoveredSide.pop(i)
                i = i - 1
                break
            else:
                continue
        i = i + 1
    return uncoveredSide

#####################################
#第三部分，在没有cover的concaveSide上做最大内接矩形
#####################################
def findMaxRecOfNonCoverSide(uncoverSideL,grid):
    rectangleList = []
    for element in uncoverSideL:
        dir=findDir(element, grid)
        rectangleList.append(Point.Rectangle(element,findMaxRecOfSide(element,grid,dir)))
    return rectangleList

#####################################
#第四部分，检测有无剩余
#####################################
# 目前想法，直接检测有哪些cell 未被cover，未被cover的必然是cell
def checkUncoveredCell(RectangleList,grid):
    temp=[] #用来存放最后生成的rectangle unit
    for element in grid.gridCellL:
        if element.holeNot==0:
            if cellCoveredOrNot(element, RectangleList)==1:
                continue
            elif cellCoveredOrNot(element, RectangleList)==0:
                temp.append(element)
                continue
    return temp

# 判断一个cell是否被cover
def cellCoveredOrNot(Cell,RectangleList):
    #将Cell转化为shapely polygon对象
    CellRectangle = createRectagnleWithShapely(Cell.XlineList,Cell.YlineList)
    if rectangleCover!=None:
        for element in RectangleList:
            x1 = (element.DiagonalPoints[0], element.DiagonalPoints[1])
            x2 = (element.DiagonalPoints[0], element.DiagonalPoints[3])
            x3 = (element.DiagonalPoints[2], element.DiagonalPoints[3])
            x4 = (element.DiagonalPoints[2], element.DiagonalPoints[1])
            tempPolygon = Polygon([x1,x2,x3,x4],)
            if CellRectangle[0].intersects(tempPolygon):#先判断是否相交
                if isinstance(CellRectangle[0].intersection(tempPolygon),Polygon):
                    # print('The point of not hole cell',list(CellRectangle[0].exterior.coords),'The Intersection rectangle is ', list(tempPolygon.exterior.coords))
                    return 1#1代表这个cell已经被rectangle覆盖
                else:
                    continue
            else:
                continue
        return 0#1代表再rectagnleList中没有任何一个unit cover这个cell
    return -1#代表Rectanlge为空

# 利用shapely将生成的网格变为一个个多边形类的列表
def createRectagnleWithShapely(xline,yline):
    tempRecList=[]
    for i in range(1,len(xline)):
        for j in range(0,len(yline)-1):
            x1 = (yline[j],xline[i])
            x2 = (yline[j], xline[i-1])
            x3 = (yline[j+1], xline[i-1])
            x4 = (yline[j+1], xline[i])
            tempList=[x1,x2,x3,x4]
            tempRecList.append(Polygon(tempList,))
    return tempRecList

#####################################
#调用之前的方法
#####################################
# 调用第一部分代码，返回一个convex side 上maximum rectangle的list（去重后)
#输入参数为Grid class的对象
def AlgorithmStage1(test):
    # 先找convexsegment的unit
    newTemp = []
    temp = findMaxRecOfConvexSegInGrid(test)
    # # 去掉第一部分结束后所得到的unit中重复的项
    LengthOfOriginalTemp = len(temp)
    for i in range(0, LengthOfOriginalTemp):
        if len(temp) != 0:
            newTemp.append(temp[0])
            del temp[0]
            for element in temp:
                if newTemp[i].DiagonalPoints == element.DiagonalPoints:
                    temp.remove(element)
                else:
                    continue
        else:
            break
    # # 去掉第一部分结束后所得到的unit中重复的项end
    return newTemp

# 调用第一部分，第二部分和第三部分代码
def AlgorithmStageOneAndTwo(test):
    newTemp=AlgorithmStage1(test)
    tempList = findUncoverConcaveSide(test, newTemp)
    if len(tempList) == 0:
        return newTemp
    temp1 = findMaxRecOfNonCoverSide(tempList, test)
    UnitList=newTemp+temp1
    return UnitList

#调用第四部分代码,该方法主要方便管理，不实现任何复杂逻辑
def AlgorithmStage3(UnitList,test):
    uncoverCellList = checkUncoveredCell(UnitList, test)
    # print(len(uncoverCellList), '111111111111')
    return uncoverCellList



# 实现可视化管理
def DrawAlgorithm1(UnitList,uncoverCellList,test):
    rectangleCover.DrawPointList(test.pointList)
    rectangleCover.DrawCellList(uncoverCellList)#第四部分结果可视化
    rectangleCover.DrawRectangleList1(UnitList)#123部分结果可视化
