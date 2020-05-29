# -*- coding: utf-8 -*-
"""
Created on 2019/10/2

@author: yhy

算法实现
《Kumar and Ramesh - 2003 - Covering Rectilinear Polygons with Axis-Parallel Rectangles》中的算法
算法适用范围：
 1.目标多边形为 RECTILINEAR POLYGONS(正交多边形)
 2.unit
    为平行于坐标轴的矩形
 3.目标多边形中可以有hole
"""
from math import sqrt
import matplotlib.pyplot as plt
from descartes import PolygonPatch
from shapely.geometry import Polygon, LineString, Point

GRAY = '#00b700'
BLUE = '#6699cc'
YELLOW = '#ffe680'
LIME = '#00FF00'


GM = (sqrt(5) - 1.0) / 2.0
W = 8.0
H = W * GM
SIZE = (W, H)

import Class,Point

#算法实现-------------
# 寻找strips,从grid中将所有的strips寻找出来进行分类
def findStrip(graph):
    # count = 0
    stripList = []
    tCell = None
    GCl = graph.gridCellL
    strip=0#标记当前是否为开始计算strip长度状态
    for i in range(len(GCl)):
        if strip == 0:
            if GCl[i].holeNot == 1:
                continue
            elif GCl[i].holeNot == 0:
                if (GCl[i].point1.coordinate[1] == graph.xlineList[-1]):
                    stripList.append(Class.strip(GCl[i], GCl[i]))
                    continue
                else:
                    strip = 1
                    tCell = GCl[i]
                    continue
        else:
            if GCl[i].holeNot == 1:
                strip = 0
                stripList.append(Class.strip(tCell,GCl[i-1]))
                continue
            else:
                if(GCl[i].point1.coordinate[1] == graph.xlineList[-1]):
                    strip = 0
                    stripList.append(Class.strip(tCell, GCl[i]))
                    continue
                else:
                    continue
    return stripList

# 实现Strip的左右扩展,direction参数表示向左或者向右，每次调用表示扩展一条
def stripExtendL(Strip,graph):
    tempCellPostion = 0
    tempCellPostion1 = 0
    # 零表示向左
    if Strip.topCell.point1.coordinate[0] > graph.ylineList[0]:
        for element in graph.gridCellL:
            if element.point4.coordinate == Strip.topCell.point1.coordinate:#前后两列point1和point4为一个点
                tempCellPostion = graph.gridCellL.index(element)
                break
        for element in graph.gridCellL:
            if element.point4.coordinate == Strip.bottomCell.point1.coordinate:  # 前后两列point1和point4为一个点
                tempCellPostion1 = graph.gridCellL.index(element)
                break
        for i in range(tempCellPostion,tempCellPostion1+1):
            if graph.gridCellL[i].holeNot == 0:
                continue
            elif graph.gridCellL[i].holeNot == 1:
                return Strip
        leftS = Class.strip(graph.gridCellL[tempCellPostion], graph.gridCellL[tempCellPostion1])
        return stripExtendL(leftS, graph)
    else:
        return Strip

def stripExtendR(Strip, graph):
    tempCellPostion = 0
    tempCellPostion1 = 0
    # 这里用point4进行比较，如果strip已经在grid的最边缘，直接返回
    if Strip.topCell.point4.coordinate[0] < graph.ylineList[-1]:
        for element in graph.gridCellL:
            if element.point1.coordinate == Strip.topCell.point4.coordinate:
                tempCellPostion = graph.gridCellL.index(element)
                break
        for element in graph.gridCellL:
            if element.point1.coordinate == Strip.bottomCell.point4.coordinate:
                tempCellPostion1 = graph.gridCellL.index(element)
                break
        for i in range(tempCellPostion,tempCellPostion1+1):
            if graph.gridCellL[i].holeNot == 0:
                continue
            elif graph.gridCellL[i].holeNot == 1:
                # print(Strip,'////////////////')
                return Strip
        rightS = Class.strip(graph.gridCellL[tempCellPostion], graph.gridCellL[tempCellPostion1])
        return stripExtendR(rightS, graph)
    else:
        return Strip

#综合步骤方法，调用之前方法得出结果
def findRectangle(graph):
    count = 0
    rectangleL = []
    tempList=findStrip(graph)
    for element in tempList:
        leftS = stripExtendL(element, graph)
        rightS = stripExtendR(element, graph)
        rectangleL.append(Class.rectangle(leftS,rightS))
        count = count + 1
    return rectangleL

#算法实现end-------------

#############################
# 输出为图像功能实现(following are visualization function)-------
#################################
def DrawPoint(Point):
    plt.plot(Point.coordinate[0], Point.coordinate[1],'o' ,color=GRAY, linewidth=1, zorder=1)

# 将点的列表组合成一个闭合图形（多边形），即起始点和终点相连
def DrawPointList(pointList):
    coordinateXList = []
    coordinateYList = []
    for i in range(len(pointList)):
        coordinateXList.append(pointList[i].coordinate[0])
        coordinateYList.append(pointList[i].coordinate[1])
    coordinateXList.append(pointList[0].coordinate[0])
    coordinateYList.append(pointList[0].coordinate[1])
    plt.plot(coordinateXList, coordinateYList, '-',color=GRAY, linewidth=3, zorder=1)

# 将点的列表组合成一个非闭合图形（polyline），即起始点和终点不需要相连
def DrawPointList1(pointList):
    coordinateXList = []
    coordinateYList = []
    for i in range(len(pointList)):
        coordinateXList.append(pointList[i].coordinate[0])
        coordinateYList.append(pointList[i].coordinate[1])
    plt.plot(coordinateXList, coordinateYList, color=GRAY, linewidth=2, zorder=1)

#-------------------------------

#绘制网格
def DrawGridLine(xOry,vertical):
    if vertical == 1:#垂直即平行于y轴
        plt.axvline(xOry, ls="--", linewidth=4,c="yellow")
    elif vertical==0:
        plt.axhline(xOry, ls="--", linewidth=4,c="yellow")  # 添加水平直线
    else:
        return

def DrawGridLineList(xOryList,vertical):
    for element in xOryList:
        DrawGridLine(element,vertical)

#-------------------------------

# 绘制cell
def DrawCell(Cell):
    coordinateXList = [Cell.point1.coordinate[0],
                       Cell.point2.coordinate[0],
                       Cell.point3.coordinate[0],
                       Cell.point4.coordinate[0],
                       Cell.point1.coordinate[0]]
    coordinateYList = [Cell.point1.coordinate[1],
                       Cell.point2.coordinate[1],
                       Cell.point3.coordinate[1],
                       Cell.point4.coordinate[1],
                       Cell.point1.coordinate[1]]
    if Cell.holeNot==1:
        plt.plot(coordinateXList, coordinateYList, color=BLUE,linewidth=1, zorder=1)
        # plt.fill_between(coordinateXList, coordinateYList, facecolor=BLUE, alpha=0.5)
    elif Cell.holeNot==0:
        plt.plot(coordinateXList, coordinateYList, color=LIME, linewidth=3, zorder=1)

def DrawCellList(CellList):
    for element in CellList:
        DrawCell(element)

#-------------------------------
# 绘制线段
def DrawSegment(Segment,ConvexOrNot):
    coordinateXList=[
        Segment.point1.coordinate[0],
        Segment.point2.coordinate[0]
    ]
    coordinateYList=[
        Segment.point1.coordinate[1],
        Segment.point2.coordinate[1]
    ]
    if ConvexOrNot==1:#是cevex的边
        plt.plot(coordinateXList, coordinateYList, color='red',linewidth=3, zorder=1)
    elif ConvexOrNot==0:
        plt.plot(coordinateXList, coordinateYList, color=BLUE, linewidth=3, zorder=1)

def DrawConvexSegmentList(SegmentList):
    for element in SegmentList:
        DrawSegment(element, 1)

def DrawConcaveSegmentList(SegmentList):
    for element in SegmentList:
        DrawSegment(element, 0)

#-------------------------------

# 基于Point包中的rectangle类， 算法2rectangle可视化方法
def DrawRectangle1(Rectangle):
    #计算中点坐标
    x = (Rectangle.DiagonalPoints[0] + Rectangle.DiagonalPoints[2]) / 2
    y = (Rectangle.DiagonalPoints[1] + Rectangle.DiagonalPoints[3]) / 2
    # coordinateXList = [ Rectangle.DiagonalPoints[0],
    #                    Rectangle.DiagonalPoints[0],
    #                    Rectangle.DiagonalPoints[2],
    #                    Rectangle.DiagonalPoints[2],
    #                    Rectangle.DiagonalPoints[0],
    #                    ]
    # coordinateYList = [Rectangle.DiagonalPoints[1],
    #                    Rectangle.DiagonalPoints[3],
    #                    Rectangle.DiagonalPoints[3],
    #                    Rectangle.DiagonalPoints[1],
    #                    Rectangle.DiagonalPoints[1],
    #                    ]
    coordinateXList = [0.1 * x + 0.9 * Rectangle.DiagonalPoints[0],
                       0.1 * x + 0.9 * Rectangle.DiagonalPoints[0],
                       1.9 * x - 0.9 * Rectangle.DiagonalPoints[0],
                       1.9 * x - 0.9 * Rectangle.DiagonalPoints[0],
                       0.1 * x + 0.9 * Rectangle.DiagonalPoints[0],
                       ]
    coordinateYList = [0.1 * y + 0.9 * Rectangle.DiagonalPoints[1],
                       1.9 * y - 0.9 * Rectangle.DiagonalPoints[1],
                       1.9 * y - 0.9 * Rectangle.DiagonalPoints[1],
                       0.1 * y + 0.9 * Rectangle.DiagonalPoints[1],
                       0.1 * y + 0.9 * Rectangle.DiagonalPoints[1],
                       ]
    # coordinateXList = [0.05 * x + 0.95 * Rectangle.DiagonalPoints[0],
    #                    0.05 * x + 0.95 * Rectangle.DiagonalPoints[0],
    #                    1.95 * x - 0.95 * Rectangle.DiagonalPoints[0],
    #                    1.95 * x - 0.95 * Rectangle.DiagonalPoints[0],
    #                    0.05 * x + 0.95 * Rectangle.DiagonalPoints[0],
    #                    ]
    # coordinateYList = [0.05 * y + 0.95 * Rectangle.DiagonalPoints[1],
    #                    1.95 * y - 0.95 * Rectangle.DiagonalPoints[1],
    #                    1.95 * y - 0.95 * Rectangle.DiagonalPoints[1],
    #                    0.05 * y + 0.95 * Rectangle.DiagonalPoints[1],
    #                    0.05 * y + 0.95 * Rectangle.DiagonalPoints[1],
    #                    ]
    # plt.plot(coordinateXList, coordinateYList,'--' ,color=YELLOW, linewidth=2, zorder=1)
    plt.plot(coordinateXList, coordinateYList, '-o', color=YELLOW, linewidth=1, zorder=1)
    plt.fill_between(coordinateXList, coordinateYList, facecolor='ivory')

# 算法1rectangle可视化方法
def DrawRectangle(Rectangle):
    #计算中点坐标
    x = (Rectangle.leftStrip.bottomCell.point1.coordinate[0]+Rectangle.rightStrip.bottomCell.point4.coordinate[0])/2
    y = (Rectangle.leftStrip.bottomCell.point1.coordinate[1]+Rectangle.leftStrip.topCell.point2.coordinate[1])/2
    coordinateXList = [0.1 * x + 0.9 * Rectangle.leftStrip.bottomCell.point1.coordinate[0],
                       0.1 * x + 0.9 * Rectangle.leftStrip.bottomCell.point1.coordinate[0],
                       1.9 * x - 0.9 * Rectangle.leftStrip.bottomCell.point1.coordinate[0],
                       1.9 * x - 0.9 * Rectangle.leftStrip.bottomCell.point1.coordinate[0],
                       0.1 * x + 0.9 * Rectangle.leftStrip.bottomCell.point1.coordinate[0],
                       ]

    coordinateYList = [0.1 * y + 0.9 * Rectangle.leftStrip.bottomCell.point1.coordinate[1],
                       1.9 * y - 0.9 * Rectangle.leftStrip.bottomCell.point1.coordinate[1],
                       1.9 * y - 0.9 * Rectangle.leftStrip.bottomCell.point1.coordinate[1],
                       0.1 * y + 0.9 * Rectangle.leftStrip.bottomCell.point1.coordinate[1],
                       0.1 * y + 0.9 * Rectangle.leftStrip.bottomCell.point1.coordinate[1],
                       ]
    plt.plot(coordinateXList, coordinateYList,'-o' ,color=YELLOW, linewidth=2, zorder=1)

# 算法1rectangle可视化方法
def DrawRectangleList(RectangleList):
    for element in RectangleList:
        DrawRectangle(element)

# 算法2rectangle可视化方法
def DrawRectangleList1(RectangleList):
    for element in RectangleList:
        DrawRectangle1(element)

#-------------------------------

# 调用 上述方法，将算法结果输出
# def DrawAlgorithm(test):
#     DrawPointList(test.pointList)
#     DrawCellList(test.holeList)
#     DrawRectangleList(findRectangle(test))

# 自己调用findRectangle(test)并返回到RectanlgeList中
def DrawAlgorithm(RectanlgeList,test):
    DrawPointList(test.pointList)
    DrawCellList(test.holeList)
    DrawRectangleList(RectanlgeList)

#############################
# 输出为图像功能实现end-------
#################################