# -*- coding: utf-8 -*-
"""
Created on 2019/10/2

@author: yhy

用来读去shape文件从而生成多边形用来检测
可以生成1000个多边形用来测试
并且转化为两种形式，网格表示和点表示
"""
import shapefile
from shapely.geometry import Polygon
from shapely.ops import unary_union
from descartes import PolygonPatch
import matplotlib.pyplot as plt
from time import *

from Point import Point
from Class import Cell,Grid
from rectangleCover import DrawCellList,DrawPointList,DrawAlgorithm,findRectangle,DrawGridLineList
from rectangleCoverAl2 import DrawAlgorithm1,AlgorithmStageOneAndTwo,AlgorithmStage3

holeList=[
    Cell(3,2,1,2)
]

# bbox为列表存放多边形的左下角的x，y坐标和右上角的x，y坐标，n为长所要分的分数，m为宽所要分的分数
def CreateYlineListForRectangle(BboxOfP,n):
    tempList=[]
    temp = BboxOfP[0]
    if len(BboxOfP) == 4:
        stepOfLength = (BboxOfP[2]-BboxOfP[0])/n
        for i in range(0,n+1):
            tempList.append(temp+(i*stepOfLength))
    return tempList

def CreateXlineListForRectangle(BboxOfP,m):
    tempList=[]
    temp = BboxOfP[1]
    if len(BboxOfP) == 4:
        stepOfHight = (BboxOfP[3] - BboxOfP[1]) / m
        for i in range(0,m+1):
            tempList.append(temp+(i*stepOfHight))
    tempList.reverse()
    return tempList

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

# n,m为长宽,用class中的类生成cellList
def createIntegerGrid(n,m,holeList):
    GridL=[]
    for j in range(0,n):
        for i in range(1, m + 1):
            GridL.append(Cell(j,i,1,1))
    # 改变list中hole的值
    for k in range(0,len(holeList)):
        if holeList[k] == 0:
            GridL[k].holeNot=0
        elif holeList[k] == 1:
            continue
        else:
            return -1
    return GridL

# 创建一个由shapely rectangle类的对象列表
def createRectagnleListWithShapely(n,m,TestPolygon):
    tempYline = CreateYlineListForRectangle(TestPolygon.bbox, n)
    tempXline = CreateXlineListForRectangle(TestPolygon.bbox, m)
    temp = createRectagnleWithShapely(tempXline, tempYline)  #可以和createRectagnleListWithShapely1方法进行代码上的优化
    return temp

# 创建一个由shapely rectangle类的对象列表
def createRectagnleListWithShapely1(n,m):
    tempYline1 = []
    tempXline1 = []
    for i in range(0, n + 1):
        tempYline1.append(i)
    for j in range(0, m + 1):
        tempXline1.append(j)
    temp1 = createRectagnleWithShapely(tempXline1, tempYline1)
    return temp1

def createHoleListWithTargetPolygon(Xcoordinate,Ycoordinate,temp):
    i = 0
    holeList = []
    tempPointList = []  # 存放从shapefile中读取的暂时数据点，用来生成多边形
    for i in range(len(Xcoordinate)):
        tempPointList.append((Xcoordinate[i], Ycoordinate[i]))
    # 用点读取到的点生成多边形
    targetP = Polygon(tempPointList,)

    for element in temp:#temp为存放着所有以cell为原型的shaply polygon 类
        if element.intersects(targetP):  # 相交代表不为hole
            holeList.append(0)
        else:
            holeList.append(1)
        i = i + 1
    return holeList

def createTargetPolygonByConbineRectanlgeList(holeList,temp1):
    temp2 = []
    for k in range(0, len(holeList)):
        if holeList[k] == 0:
            temp2.append(temp1[k])

    # 将他们组合起来为一个多边形
    u = unary_union(temp2)
    unionPL = list(u.exterior.coords)
    temp3 = []
    for element in unionPL:
        temp3.append(Point(element[0], element[1]))
    return temp3

# 定义方法精炼顶点,目前再总方法中实现

#读取shape文件 ,目前规定一个死目录
def ReadShapefile():
    border_shape = shapefile.Reader("E:/Desktop/project/shaefile/AUS_adm2.shp")
    border = border_shape.shapes()
    return border

# 读取shape文件并且将转化好的正交多边形（用point表示方法）存入本地文件，n,m 分别表示希望
#参数表示将多边形的长和宽分为多少份-
# 该方法调用算法1
def SavePolygonToLocal(n,m):
    # 通过创建reader类的对象进行shapefile文件的读取
    saveLocal = 'fig cover AL1/'+str(n)+'x'+str(m)
    border = ReadShapefile()
    # .shapes()读取几何数据信息，存放着该文件中所有对象的 几何数据
    # border是一个列表
    print(len(border))
    # 返回第1个对象的所有点坐标
    # border_points = [(x1,y1),(x2,y2),(x3,y3),…]
    # 将点组合
    # 根据读取的border中的元素构造的shapely rectagnle类的多边形
    f = open('E:/Desktop/project/fig/'+saveLocal+'/time.txt', "w")
    f1 = open('E:/Desktop/project/fig/' + saveLocal + '/unitNum.txt', "w")
    # for i in range(0, len(border)):
    for i in range(0, len(border)):
        fig = plt.figure(figsize=(10,10))#每次循环都建立一张新的图片
        TestPolygon = border[i]
        border_points = TestPolygon.points
        x, y = zip(*border_points)
        temp = createRectagnleListWithShapely(n, m, TestPolygon)
        # 根据份数构造的shapely rectagnle类的多边形
        temp1 = createRectagnleListWithShapely1(n, m)
        holeList = createHoleListWithTargetPolygon(x, y, temp)
        # 将holelist中为1的元素对应到temp1中的多边形提炼出来
        temp3 = createTargetPolygonByConbineRectanlgeList(holeList, temp1)
        # 将temp3中的点精炼为只有多边形顶点的列表，目前是存储所有的点
        j = 0
        while (1):
            if j < len(temp3) - 1:
                if temp3[j - 1].coordinate[0] == temp3[j].coordinate[0] and temp3[j].coordinate[0] == \
                        temp3[j + 1].coordinate[0]:
                    del temp3[j]
                    continue
                elif temp3[j - 1].coordinate[1] == temp3[j].coordinate[1] and temp3[j].coordinate[1] == \
                        temp3[j + 1].coordinate[1]:
                    del temp3[j]
                    continue
                else:
                    j = j + 1
                    continue
            elif j == len(temp3) - 1:
                if temp3[j - 1].coordinate[0] == temp3[j].coordinate[0] and temp3[j].coordinate[0] == \
                        temp3[0].coordinate[0]:
                    del temp3[j]
                    continue
                elif temp3[j - 1].coordinate[1] == temp3[j].coordinate[1] and temp3[j].coordinate[1] == \
                        temp3[0].coordinate[1]:
                    del temp3[j]
                    continue
                else:
                    j = j + 1
                    continue
            else:
                break
        test = Grid([], temp3)
        start = time()
        RectanlgeList=findRectangle(test)#调用算法一
        end = time()
        DrawAlgorithm(RectanlgeList,test)
        # DrawPointList(temp3)
        spendTime=(end - start)
        f.write("("+str(spendTime)+","+str(i)+")\n")
        f1.write("("+str(len(RectanlgeList))+","+str(i)+")\n")
        # plt.savefig('E:/Desktop/project/fig/'+saveLocal+'/' + str(i) + '.png')
        print(i,spendTime)
        # plt.show()
        plt.close(fig)
    f.close()
    f1.close()

# 该方法调用算法2
def SavePolygonToLocal1(n,m):
    # 通过创建reader类的对象进行shapefile文件的读取
    saveLocal = 'fig cover AL2/'+str(n)+'x'+str(m)
    border = ReadShapefile()
    # .shapes()读取几何数据信息，存放着该文件中所有对象的 几何数据
    # border是一个列表
    print(len(border))
    # 返回第1个对象的所有点坐标
    # border_points = [(x1,y1),(x2,y2),(x3,y3),…]
    # 将点组合
    # 根据读取的border中的元素构造的shapely rectagnle类的多边形
    f = open('E:/Desktop/project/fig/' + saveLocal + '/time.txt', "w")
    f1 = open('E:/Desktop/project/fig/' + saveLocal + '/unitNum.txt', "w")
    # for i in range(0, len(border)):
    for i in range(0, len(border)):
        # fig = plt.figure(figsize=(10,10))#每次循环都建立一张新的图片
        TestPolygon = border[i]
        border_points = TestPolygon.points
        x, y = zip(*border_points)
        temp = createRectagnleListWithShapely(n, m, TestPolygon)
        # 根据份数构造的shapely rectagnle类的多边形
        temp1 = createRectagnleListWithShapely1(n, m)
        holeList = createHoleListWithTargetPolygon(x, y, temp)
        # 将holelist中为1的元素对应到temp1中的多边形提炼出来
        temp3 = createTargetPolygonByConbineRectanlgeList(holeList, temp1)

        # for element in temp3:
        #      print(element.coordinate)
        # print('len of temp3',len(temp3))
        #-----------------
        # 将temp3中的点精炼为只有多边形顶点的列表，目前是存储所有的点
        j=0
        while(1):
            if j < len(temp3)-1:
                if temp3[j-1].coordinate[0]==temp3[j].coordinate[0] and temp3[j].coordinate[0]==temp3[j+1].coordinate[0]:
                    del temp3[j]
                    continue
                elif temp3[j-1].coordinate[1]==temp3[j].coordinate[1] and temp3[j].coordinate[1]==temp3[j+1].coordinate[1]:
                    del temp3[j]
                    continue
                else:
                    j=j+1
                    continue
            elif j == len(temp3)-1:
                if temp3[j-1].coordinate[0]==temp3[j].coordinate[0] and temp3[j].coordinate[0]==temp3[0].coordinate[0]:
                    del temp3[j]
                    continue
                elif temp3[j-1].coordinate[1]==temp3[j].coordinate[1] and temp3[j].coordinate[1]==temp3[0].coordinate[1]:
                    del temp3[j]
                    continue
                else:
                    j=j+1
                    continue
            else:
                break
        # print('len of temp3', len(temp3))
        test = Grid([], temp3)
        # DrawPointList(temp3)
        # ------设置坐标间隔
        # x_major_locator = plt.MultipleLocator(1)
        # # 把x轴的刻度间隔设置为1，并存在变量里
        # y_major_locator = plt.MultipleLocator(1)
        # # 把y轴的刻度间隔设置为10，并存在变量里
        # ax = plt.gca()
        # # ax为两条坐标轴的实例
        # ax.xaxis.set_major_locator(x_major_locator)
        # # 把x轴的主刻度设置为1的倍数
        # ax.yaxis.set_major_locator(y_major_locator)
        # ------设置坐标间隔end-------
        # ---------------------
        start = time()
        # 算法二
        UnitList = AlgorithmStageOneAndTwo(test)
        uncoverCellList = AlgorithmStage3(UnitList, test)
        end = time()
        # DrawAlgorithm1(UnitList, uncoverCellList, test)
        spendTime = end-start
        print(type(spendTime))
        f.write("("+str(spendTime)+","+str(i)+")\n")
        f1.write("("+str(len(UnitList)+len(uncoverCellList))+","+str(i)+")\n")
        # plt.savefig('E:/Desktop/project/fig/'+saveLocal+'/' + str(i) + '.png')
        print(i)
        # plt.show()
        # plt.close(fig)
    f.close()
    f1.close()


# 输出原有图像
def SavePolygonToLocal2(n,m):
    # 通过创建reader类的对象进行shapefile文件的读取
    saveLocal = 'fig origin/'+str(n)+'x'+str(m)
    border = ReadShapefile()
    # .shapes()读取几何数据信息，存放着该文件中所有对象的 几何数据
    # border是一个列表
    print(len(border))
    # 返回第1个对象的所有点坐标
    # border_points = [(x1,y1),(x2,y2),(x3,y3),…]
    # 将点组合
    # 根据读取的border中的元素构造的shapely rectagnle类的多边形
    # f = open('E:/Desktop/project/fig/' + saveLocal + '/NumOfP.txt', "w")
    # for i in range(0, len(border)):
    for i in range(58, 59):
        fig = plt.figure(figsize=(10,10))#每次循环都建立一张新的图片
        TestPolygon = border[i]
        border_points = TestPolygon.points
        x, y = zip(*border_points)
        temp = createRectagnleListWithShapely(n, m, TestPolygon)
        # 根据份数构造的shapely rectagnle类的多边形
        temp1 = createRectagnleListWithShapely1(n, m)
        holeListOfTargetPolygonGrid = createHoleListWithTargetPolygon(x, y, temp)
        # 将holelist中为1的元素对应到temp1中的多边形提炼出来
        temp3 = createTargetPolygonByConbineRectanlgeList(holeListOfTargetPolygonGrid, temp1)
        #-----
        j = 0
        while (1):
            if j < len(temp3) - 1:
                if temp3[j - 1].coordinate[0] == temp3[j].coordinate[0] and temp3[j].coordinate[0] == \
                        temp3[j + 1].coordinate[0]:
                    del temp3[j]
                    continue
                elif temp3[j - 1].coordinate[1] == temp3[j].coordinate[1] and temp3[j].coordinate[1] == \
                        temp3[j + 1].coordinate[1]:
                    del temp3[j]
                    continue
                else:
                    j = j + 1
                    continue
            elif j == len(temp3) - 1:
                if temp3[j - 1].coordinate[0] == temp3[j].coordinate[0] and temp3[j].coordinate[0] == \
                        temp3[0].coordinate[0]:
                    del temp3[j]
                    continue
                elif temp3[j - 1].coordinate[1] == temp3[j].coordinate[1] and temp3[j].coordinate[1] == \
                        temp3[0].coordinate[1]:
                    del temp3[j]
                    continue
                else:
                    j = j + 1
                    continue
            else:
                break
        #------
        # test = Grid(holeList, temp3)
        # # plt.grid(ls=":", c='b', )#打开坐标网格
        # DrawGridLineList(test.xlineList,0)
        # DrawGridLineList(test.ylineList,1)
        DrawPointList(temp3)
        # DrawCellList(holeList)
        # # ------设置坐标间隔
        # x_major_locator = plt.MultipleLocator(1)
        # # 把x轴的刻度间隔设置为1，并存在变量里
        # y_major_locator = plt.MultipleLocator(1)
        # # 把y轴的刻度间隔设置为10，并存在变量里
        # ax = plt.gca()
        # # ax为两条坐标轴的实例
        # ax.xaxis.set_major_locator(x_major_locator)
        # # 把x轴的主刻度设置为1的倍数
        # ax.yaxis.set_major_locator(y_major_locator)
        # # ------设置坐标间隔end-------
        # # ---------------------
        plt.savefig('E:/Desktop/project/fig/'+saveLocal+'/' + str(i) + '.png')
        plt.show()
        # f.write("(" + str(len(temp3)) + "," + str(i) + ")\n")
        print(i)
        plt.close(fig)
    # f.close()

if __name__ == '__main__':
    z=100
    # SavePolygonToLocal(z,z)
    # SavePolygonToLocal1(z,z)
    SavePolygonToLocal2(z,z)
    print('finished111111')


