# -*- coding: utf-8 -*-
"""
Created on 2019/10/2

@author: yhy
类定义：
1.cell类
2.strip类
3.rectangle类
4.grid类，也是就是图像类，用来创建一个多边形和其所在网格(grid)

存在问题2020.3.4:
如果一个grid类在定义的时候，给定的在多边形内部的hole如果是有一条边与多边形的边重叠的话
此时多边形的边应该更新为hole中不与其重叠的另外三个边。多边形的顶点也应该发生变化。
然而，该程序目前并不能完成这一功能，也就是说系统依然判定，多边形的被重叠边为多边形边界
总而言之就是存在hole与多边形有边的重叠，这是不规范的


"""
import Point

class Cell:
    # x,y是每个cell左下角的横纵坐标
    def __init__(self,x,y,l,h):
        # 点属性坐标顺序0,1，2，3分别为左下，左上，右上，右下
        self.point1 = Point.Point(x,y)
        self.point2 = Point.Point(x,y+h)
        self.point3 = Point.Point(x+l,y+h)
        self.point4 = Point.Point(x+l,y)
        # 表示是否为hole，1是，0否
        self.holeNot= 1
        self.length = l
        self.height = h
        # 列表存贮
        self.point = [self.point1,self.point2,self.point3,self.point4]
        # 线属性，xline是纵坐标集合，yline是横坐标集合
        self.XlineList = [self.point1.xline,self.point3.xline]
        self.YlineList = [self.point1.yline,self.point3.yline]

class strip:
    def __init__(self,tCell,bCell):
        self.topCell=tCell
        self.bottomCell=bCell
        # 表示有几个cell，如只有一个cell的strip就是1,//属性目前有问题
        # self.height = (self.topCell.point1.coordinate[1]-self.bottomCell.point1.coordinate[1])+1

# 特指由两个strip形成的矩形，在算法1中
class rectangle:
    def __init__(self,stripL,stripR):
        self.leftStrip = stripL
        self.rightStrip = stripR
        self.DiagonalPoints =self.findDiagonalPoints()
    def findDiagonalPoints(self):
        temp=[self.leftStrip.bottomCell.point1.coordinate[0],
              self.leftStrip.bottomCell.point1.coordinate[1],
              self.rightStrip.topCell.point3.coordinate[0],
              self.rightStrip.topCell.point3.coordinate[1],
              ]
        return temp


# 网格类，主要储存正交多边形就是一个正交多边形对应一个网格
class Grid:
    def __init__(self,holeList,pointList):
        # 图像的每个拐点，list保存,注意该列表中存贮的是点实例
        self.pointList = pointList
        #多边形内部的hole 所组成的list
        self.holeList = holeList
        # 多边形的边，该列表中存放的是线段的实例
        self.segmentList = self.createSegmentlist()
        # 找出一个图形中所有顶点，从而确定grid有几条横线竖线，使用列表存储
        self.xlineList=self.createXlineList(self.holeList,pointList)
        self.ylineList=self.createYlineList(self.holeList,pointList)
        # 列数
        self.height = len(self.ylineList)-1
        # 行数
        self.length = len(self.xlineList)-1

        #网格存放一个grid中的所有cell实列的列表
        self.gridCellL = self.createGridC(self.xlineList,self.ylineList)

        #所有Hole列表
        self.allHoleL = self.createAllHoleL()

        #新建属性2020.3.4，列表用来存储polygon中的所有convex角的list
        self.convexAngleL = []

        # 新建属性2020.3.4，列表用来存储polygon中的所有concave角的list
        self.concaveAngleL = []
        self.findPointWithOneCell()

        #新建属性2020.3.5， 用来存放convex边和concave边
        self.concaveSegmentL = []
        self.convexSegmentL = []
        self.findConcaveEdge()

    # 如果两个及以上的点在横向或纵向的方向上共线，那么就只能产生一条横线或纵线
    # 注意xlineList中的元素作为纵坐标，xline指平行于x轴的线的集合
    def createXlineList(self,holeList,pointList):
        temp=[]
        for element in holeList:
            if element.XlineList[0] not in set(temp):
                temp.append(element.XlineList[0])
            if element.XlineList[1] not in set(temp):
                temp.append(element.XlineList[1])
        for element in pointList:
            if element.xline not in set(temp):
                temp.append(element.xline)
            else:
                continue
        temp.sort(reverse=True)
        return temp

    def createYlineList(self,holeList,pointList):
        temp = []
        for element in holeList:
            if element.YlineList[0] not in set(temp):
                temp.append(element.YlineList[0])
            if element.YlineList[1] not in set(temp):
                temp.append(element.YlineList[1])
        for element in pointList:
            if element.yline not in set(temp):
                temp.append(element.yline)
            else:
                continue
        temp.sort()
        return temp

######################
# 创建一个cellList
#####################
    def createGridC(self,xline,yline):
        temp=[]
        for i in range(len(yline)-1):
            for j in range(1,len(xline)):
                # 少存一格交点坐标，及最上面的xline和最右边的yline不用计入
                temp.append(Cell(yline[i],xline[j],yline[i+1]-yline[i],xline[j-1]-xline[j]))
        return temp
####################################
# 用来建立一个包含多边形每个边的List，即多边形每一条边都是一个segment
#####################################
    def createSegmentlist(self):
        temp=[]
        for i in range(len(self.pointList)):
            if i != len(self.pointList)-1:
                temp.append(Point.Segment(self.pointList[i],self.pointList[i+1]))
            else:
                temp.append(Point.Segment(self.pointList[i],self.pointList[0]))
        return temp

##############################
#一下为判断一个cell是否在多边形内部
################################
    # 计算一个cell的中心点，方便用来进行cell是否在多边形内部
    def cellCertreP(self,cell):
        y = ((cell.point3.coordinate[1] - cell.point1.coordinate[1])/2)+ cell.point1.coordinate[1]
        x = ((cell.point3.coordinate[0] - cell.point1.coordinate[0])/2)+ cell.point1.coordinate[0]
        return Point.Point(x, y)

    # 生成一条横线线段
    def createSegment(self,point1, xCoordinate):
        return Point.Segment(point1, Point.Point(xCoordinate, point1.coordinate[1]))

    # 生成一条竖线线段
    def createSegmentVertical(self,point1, yCoordinate):
        return Point.Segment(point1, Point.Point(point1.coordinate[0],yCoordinate))

    # 判断两条线段是否相交，这里主要是垂直和水平的线段相比较
    def intersectOrNot(self,segment1, segment2):
        p1 = segment1.point1.coordinate
        p2 = segment1.point2.coordinate
        p3 = segment2.point1.coordinate
        p4 = segment2.point2.coordinate

        if min(p3[1], p4[1]) > max(p1[1], p2[1]) or max(p3[1], p4[1]) < min(p1[1], p2[1]):
            return False
        else:
            if min(p1[0], p2[0]) > max(p3[0], p4[0]) or max(p1[0], p2[0]) < min(p3[0], p4[0]):
                return False
            else:
                return True

    # 根据一个cell的线段是否与多边形的边的交点个数判断是否在多边形内部，在外部就是hole
    def holeOrNot(self,cell):
        count = 0
        segment1 = self.createSegment(self.cellCertreP(cell), self.ylineList[-1])
        for element in self.segmentList:
            if self.intersectOrNot(segment1, element):
                count = count + 1
        if (count % 2) == 0:
            return True
        else:
            for element in self.holeList:
                # 为判断一个cell是否在holeList里出现过，进行一下比较
                if element.point1.coordinate[0] == cell.point1.coordinate[0]:
                    if cell.point1.coordinate[1] >= element.point1.coordinate[1] and cell.point1.coordinate[1] < element.point2.coordinate[1]:
                        return True
                    else:
                        continue
                else:
                    continue
            return False

    # 将所有的hole整合起来，闯将一个holeList,包括在多边形外部的区域
    def createAllHoleL(self):
        temp=[]
        for element in self.gridCellL:
            if self.holeOrNot(element):
                temp.append(element)
            else:
                element.holeNot=0
                continue
        return temp

#####################
##以下方法实现凹凸角的分离
####################
    # 寻找多边形的顶点被几个在多边形内部的cell共享,并且由此得到角度的凹凸
    def findPointWithOneCell(self):
        for element in self.pointList:
            count = 0
            for cell in self.gridCellL:
                if cell.holeNot==0:
                    if self.pointOnCellOrNot(cell,element):
                        count = count + 1
                        continue
                    else:
                        continue
                else:
                    continue
            if count > 1:
                self.concaveAngleL.append(element)
            else:
                self.convexAngleL.append(element)


    # 该方法判断一个点是否为一个cell的四个点中的其中一个
    def pointOnCellOrNot(self,cell,point):
        if cell.point1.PointsEqualOrNot(point):
            return True
        elif cell.point2.PointsEqualOrNot(point):
            return True
        elif cell.point3.PointsEqualOrNot(point):
            return True
        elif cell.point4.PointsEqualOrNot(point):
            return True
        else:
            return False



    #实现凹凸边的分离
    def findConcaveEdge(self):
        for element in self.segmentList:
            for i in range(len(self.concaveAngleL)):
                if element.point1.PointsEqualOrNot(self.concaveAngleL[i]):
                    self.concaveSegmentL.append(element)
                    break
                elif element.point2.PointsEqualOrNot(self.concaveAngleL[i]):
                    self.concaveSegmentL.append(element)
                    break
                elif i == len(self.concaveAngleL)-1:
                    self.convexSegmentL.append(element)
                else:
                    continue



