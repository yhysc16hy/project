'''
1.点的当前坐标，从x为零开始
   点的下一次移动方向确定：
        四个方向随机，不能是来的方向

   点方向确定后的移动长度：
        长度随机（1，2，3）
    计算在该方向下，该长度下点是否超出格子
        如果是将点移动到同轴的格子边缘

还有一个情况要避免
    走的点走到原来走过的路径上

停止条件
    点的纵坐标达到最大

2020.2.26
存在问题：
起始点如果向上下移动的时候，存在衔接问题（暂时解决）

2020.2.28
存在问题：
不能保证在算法一定能完成，也就是递归可能一直调用直到溢出
    解决思路：
    1.记录点到边界的距离，使得点始终在格子范围内，不会超出格子
    2.根据点走过的折路次数停止
    目前解决方法：
    将向左移动的可能性删除，点只能向右移动，或者上下移动
'''
import random
import rectangleCover
import matplotlib.pyplot as plt
from Point import Point
from Class import Cell,rectangle,Grid

# random.seed(5)#给随机数一个固定值，方便调试
direction={1:'left',2:'up',3:'right',4:'down'}
Cell_neighbor = {'left_extensible':1,'top_extensible':2,'right_extensible':3,'bottom_extensible':4}
Cell_neighbor1 = {1:'left_extensible',2:'top_extensible',3:'right_extensible',4:'bottom_extensible'}

# 创建一个递增列表
def createIntList(rightEdge):
    x_axis=[]
    for i in range(0,rightEdge):
        x_axis.append(i)
    return x_axis


# 在一个x轴坐标是0到4，而y轴坐标取值是在0到9之间的网格里寻找多边形的一半
x_axis=createIntList(20)
y_axis=[0,1,2,3,4,5,6,7,8]

# 1.点的起始坐标，在y轴上开始，也就是x值为零，y值随机
x_startPos=0
y_startPos = random.sample(y_axis, 1)[0]

pointStart=Point(x_startPos,y_startPos)
comingDirection=0 #0代表无来时移动方向

PointList = []

#
x_axis1=createIntList(20)
y_axis1=[9,10,11,12,13,14,15]

x_startPos1=0
y_startPos1 = random.sample(y_axis1, 1)[0]

pointStart1=Point(x_startPos1,y_startPos1)

PointList1 = []

#确定点的移动方向
# 1.检测点是否在定义的格子的边界处
def onMarginOrNot(point,x_axis,y_axis):
    marginList=[]
    if point.coordinate[0]==x_axis[0]:
        marginList.append(1)
    if point.coordinate[1]==y_axis[-1]:
        marginList.append(2)
        if 1 not in marginList: #在坐标边缘减去一个方向，在坐标上边缘和下边缘时不能向左走，只能向坐标增大方向走，在下边界同理
            marginList.append(1)
    if point.coordinate[1]==y_axis[0]:
        marginList.append(4)
        if 1 not in marginList:
            marginList.append(1)
    return marginList #返回值为不可移动方向列表

def createMovingDirectionList(comingDirection,marginList):
    # 判断来时方向，确定移动方向,和来时方向相同或者相反的方向都无法作为下一次前进方向
    if comingDirection == 1 or comingDirection == 3:
        movingDirectionList = [2, 4]
    elif comingDirection == 2 or comingDirection == 4:
        movingDirectionList = [3]
    else:
        movingDirectionList = [3] #当方向为零，也就是startpoint时，只能向右移动
#根据marginList，将不可移动方向删除
    for element in marginList:
        if element in movingDirectionList:
            movingDirectionList.remove(element)
    return movingDirectionList

# 根据数组选择一个方向
def chooseDir(movingDirectionList):
    if len(movingDirectionList)==1:
        return movingDirectionList[0]
    else:
        return random.sample(movingDirectionList, 1)[0]

# print(chooseDir(createMovingDirectionList(comingDirection,onMarginOrNot(pointStart))))

#确定移动方向长短，先规定只在123，中随机产生一个
def chooseStepSize():
    return random.randint(1,3)

#
def moving(point,StepSize,direction):
    if direction == 1:
        x = point.coordinate[0] - StepSize
        y = point.coordinate[1]
    elif direction == 2:
        x = point.coordinate[0]
        y = point.coordinate[1] + StepSize
    elif direction == 3:
        x = point.coordinate[0] + StepSize
        y = point.coordinate[1]
    elif direction == 4:
        x = point.coordinate[0]
        y = point.coordinate[1] - StepSize
    return Point(x,y)

# 检查点移动后是否超出边界,并且移动到边缘
def checkOutOfGridNot(point,x_axis,y_axis):
    if point.coordinate[0] < x_axis[0]:
        point.coordinate[0] = x_axis[0]
    if point.coordinate[1] > y_axis[-1]:
        point.coordinate[1] = y_axis[-1]
    if point.coordinate[1] < y_axis[0]:
        point.coordinate[1] = y_axis[0]
    if point.coordinate[0] > x_axis[-1]:
        point.coordinate[0] = x_axis[-1]
    x = point.coordinate[0]
    y = point.coordinate[1]
    return Point(x,y)



def createMovingList(Point,comingDirection,PointList,x_axis,y_axis):
    PointList.append(Point)
    if Point.coordinate[0] == x_axis[-1]:
        return
    DirTemp=chooseDir(createMovingDirectionList(comingDirection, onMarginOrNot(Point,x_axis,y_axis)))
    point_temp = moving(Point, chooseStepSize(),DirTemp)
    point_temp = checkOutOfGridNot(point_temp,x_axis,y_axis)
    createMovingList(point_temp,DirTemp,PointList,x_axis,y_axis)

# -------------------------------
# 调用环节
# point1=moving(pointStart,chooseStepSize(),chooseDir(createMovingDirectionList(comingDirection,onMarginOrNot(pointStart))))
# rectangleCover.DrawPoint(pointStart)
# rectangleCover.DrawPoint(point1)

createMovingList(pointStart,comingDirection,PointList,x_axis,y_axis)
createMovingList(pointStart1,comingDirection,PointList1,x_axis1,y_axis1)
PointList1.reverse()

temp = PointList+PointList1
test=Grid([],temp)
rectangleCover.DrawAlgorithm(test)

plt.show()


