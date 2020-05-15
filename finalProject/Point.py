# -*- coding: utf-8 -*-
"""
Created on 2019/10/2

@author: yhy
类定义：
1.点类
2.线段类
"""
class Point:
    def __init__(self,x,y):
        self.coordinate = [x,y]
        # 一个点的纵线是横坐标，横线是纵坐标
        self.xline=y
        self.yline=x

    # 判断两个点是否相等,该方法之后可以移出grid类
    def PointsEqualOrNot(self,point):
        if self.coordinate[0] == point.coordinate[0]:
            if self.coordinate[1] == point.coordinate[1]:
                return True
            else:
                return False
        else:
            return False

# 线段
class Segment:
    def __init__(self,point1,point2):
        self.point1 = point1
        self.point2 = point2
        self.length = self.createLength()
    #     新添加属性 2020.3.6
        self.slope=self.calculateSlope()
        self.verticeOrNot = self.setVerticeValue()
        self.resetTheCoordinate()#改变segment坐标位置关系

    # 新功能，检查segment两个点的关系，保证线段的两个坐标的，总是p1的横坐标大于p2,在垂直状态下,p1在p2上面
    #只考虑了垂直和水平两种情况
    def resetTheCoordinate(self):
        temp_x = 0
        temp_y = 0
        if self.verticeOrNot==1:
            if self.point1.coordinate[1] < self.point2.coordinate[1]:
                temp_x = self.point1.coordinate[0]
                temp_y = self.point1.coordinate[1]
                self.point1 = Point(self.point2.coordinate[0], self.point2.coordinate[1])
                self.point2 = Point(temp_x,temp_y)
                return
            else:
                return
        else:
            if self.point1.coordinate[0]<self.point2.coordinate[0]:
                temp_x = self.point1.coordinate[0]
                temp_y = self.point1.coordinate[1]
                self.point1 = Point(self.point2.coordinate[0], self.point2.coordinate[1])
                self.point2 = Point(temp_x,temp_y)
                return
            else:
                return

    # 计算线段斜率
    def calculateSlope(self):
        if (self.point1.coordinate[0] - self.point2.coordinate[0]) != 0:
            return (self.point1.coordinate[1] - self.point2.coordinate[1])/(self.point1.coordinate[0] - self.point2.coordinate[0])
        else:
            return 0

    # 记录线段是否垂直，因为垂直线段斜率无法计算
    def setVerticeValue(self):
        if (self.point1.coordinate[0] - self.point2.coordinate[0])==0:
            return 1
        else:
            return 0
    # 计算线段长度
    def createLength(self):
        x_2= (self.point2.coordinate[0] - self.point1.coordinate[0])**2
        y_2= (self.point2.coordinate[1] - self.point1.coordinate[1])**2
        return (x_2+y_2)**0.5

# 算法二生成的矩形unit
class Rectangle:
    def __init__(self,LSegment,RSegment):
        #这里的leftsegment和rightsegment只是名字，并不代表其确定的位置关系，可能存在leftside是上边界，rightside是下边界
        self.leftSegment = LSegment
        self.rightSegment = RSegment
        self.SegmentL1R1 = Segment(self.leftSegment.point1,self.rightSegment.point1)
        self.SegmentL2R2 = Segment(self.leftSegment.point2, self.rightSegment.point2)
        #选出一个rectangle的对角点，规定为一个矩形左下角和右上角的点，这个属性可以用来对比矩形是否相同
        #属性四个位置分别为左下角横坐标，纵坐标，右上角横坐标，纵坐标
        self.DiagonalPoints=self.findDiagonalPoints()
    def findDiagonalPoints(self):
        temp=[0,0,0,0]
        if self.leftSegment.point1.coordinate[0]==self.rightSegment.point1.coordinate[0]:
            temp[2]=self.leftSegment.point1.coordinate[0]
            temp[0] = self.leftSegment.point2.coordinate[0]
            if self.leftSegment.point1.coordinate[1]>self.rightSegment.point1.coordinate[1]:
                temp[1]=self.rightSegment.point1.coordinate[1]
                temp[3]=self.leftSegment.point1.coordinate[1]
            else:
                temp[3] = self.rightSegment.point1.coordinate[1]
                temp[1] = self.leftSegment.point1.coordinate[1]
        else:
            temp[3]=self.leftSegment.point1.coordinate[1]
            temp[1]=self.leftSegment.point2.coordinate[1]
            if self.leftSegment.point1.coordinate[0]>self.rightSegment.point1.coordinate[0]:
                temp[2] = self.leftSegment.point1.coordinate[0]
                temp[0]= self.rightSegment.point1.coordinate[0]
            else:
                temp[0] = self.leftSegment.point1.coordinate[0]
                temp[2] = self.rightSegment.point1.coordinate[0]
        return temp



'''
目前构想：
新建一个角类：
    类中有一个属性表明目前这个角是在多边形内部还是外部

'''

# 这个类中的两条线段必须有交点，暂不支持无交点的两条线段创建该类
# 一个和角有关的类
class angle:
    def __init__(self,segment1,segment2):
        self.segment1= segment1
        self.segment2= segment2
        self.intersectionP = 0
        self.angle = 0