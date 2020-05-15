# -*- coding: utf-8 -*-
"""
Created on 2019/10/2

@author: yhy

用来读去shape文件从而生成多边形用来检测
可以生成1000个多边形
不同于shapefile1的方法
"""

import shapefile
from Point import Point
from Class import Grid
from rectangleCover import DrawPointList,DrawCellList,DrawCell
from matplotlib import pyplot as plt

border_shape=shapefile.Reader("E:/Desktop/project/shaefile/AUS_adm2.shp")
#通过创建reader类的对象进行shapefile文件的读取

border=border_shape.shapes()


# .shapes()读取几何数据信息，存放着该文件中所有对象的 几何数据
#border是一个列表

print(border[2].shapeType,'11111')
print(border[2].bbox,'11111')
border_points = border[2].points
#返回第1个对象的所有点坐标
#border_points = [(x1,y1),(x2,y2),(x3,y3),…]

x,y = zip(*border_points)

print(len(x),'111111')
temp = []

for i in range(len(x)):
    temp.append(Point(x[i],y[i]))
print(len(temp))

grid1 = Grid([],temp)
# for i in range(len(x)):
#     print((x[i - 1] - x[i]))
#     print((y[i - 1] - y[i]))
#     print('\n')
#x=(x1,x2,x3,…)
#y=(y1,y2,y3,…)

fig = plt.figure()
#
# ax = fig.subplots() # 生成一张图和一张子图
# plt.plot(x,y,'k-') # x横坐标 y纵坐标 ‘k-’线性为黑色
# plt.grid()# 添加网格线
# plt.axis('equal')
for element in grid1.gridCellL:
    if element.holeNot == 0:
        DrawCell(element)
# DrawCellList(grid1.gridCellL)

plt.xlim((153.0316619873047,153.12634277343756))
plt.ylim((-27.721912384033203,-27.686601638793878))
# DrawPointList(temp)

plt.show()
