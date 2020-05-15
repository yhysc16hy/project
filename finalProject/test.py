
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
import numpy as np
import copy
import xlsxwriter
import os


from rectangleCover import DrawAlgorithm,DrawRectangle1,findRectangle,DrawCellList,DrawRectangleList,\
    DrawConvexSegmentList,DrawConcaveSegmentList,DrawRectangleList1
from Point import Point,Segment,Rectangle
from Class import Cell,rectangle,Grid
from rectangleCoverAl2 import AlgorithmStageOneAndTwo,AlgorithmStage3,AlgorithmStage1,findUncoverConcaveSide,findMaxRecOfNonCoverSide


# 点的输入规则必须是按照顺序排列，也就是前后列表两个位置的点十多边形的一条边

# 测试组1
pointList=[Point(0,0),Point(0,4),Point(8,4),Point(8,0)]

holeList=[
    Cell(0,2,1,1),
    Cell(4,3,1,1),
    Cell(7,0,1,1)
]

test = Grid(holeList,pointList)

#测试组2
pointList1 = [Point(0,0),Point(2,0),Point(2,-1),
              Point(5,-1),Point(5,0),Point(6,0),
              Point(6,3),Point(8,3),Point(8,7),
              Point(10,7),Point(10,9),Point(8,9),
              Point(8,8),Point(5,8),Point(5,10),
            Point(4,10),Point(4,9),Point(2,9),Point(2,7),
              Point(-1,7),Point(-1,5),Point(1,5),
              Point(1,4),Point(0,4)]
holeList1=[
    Cell(2,6,1,1),
    Cell(2,3,1,1),
    Cell(3,3,1,2),
    Cell(5,5,1,2)
]

test1 = Grid(holeList1,pointList1)
test12=Grid([],pointList1)

# 测试组3
pointList2=[
        Point(0,1),Point(1,1),Point(1,3),
        Point(2,3),Point(2,0),Point(3,0),
        Point(3,2),Point(5,2),Point(5,1),
        Point(7,1),Point(7,0),Point(9,0),
        Point(9,5),Point(8,5),Point(8,7),
        Point(5,7),Point(5,9),Point(3,9),
        Point(3,8),Point(0,8)
]
holeList2=[]
test2 = Grid(holeList2,pointList2)

# 测试组4
pointList3=[
        Point(0,4),Point(3,4),Point(3,2),
        Point(6,2),Point(6,4),Point(7,4),
        Point(7,1),Point(8,1),Point(8,2),
        Point(9,2),Point(9,9),Point(8,9),
        Point(8,8),Point(5,8),Point(5,9),
        Point(2,9),Point(2,7),Point(0,7)
]
holeList3=[]
test3 = Grid([],pointList3)

#####
#基础方法实现
#####

#全局变量-----------------------------
RectangleSizeList=[10,20,30,40,50,60,70,80,90,100]
# 将图片和文件保存到那个文件夹
Savelocation1 = "C:/Users/Administrator/Desktop/figure1/3/"
# 哪个算法
TheMaxOfY=[
    10,400,400
]

SaveWhichAl = [
    "al1/",
    "al2/",
    "",
]
# 什么类型
SaveASWhatName = [
    ' time',
    ' unitNum',
    ' vertexNum'
]
#-----------------------------


# 读取文件，并且存储为列表形式
# whichFile,1代表time，2代表unitNum，3代表NumOfp
#whichDir，1代表算法1，2代表算法2，3，代表原数据
def readFile(n,m,whichFile,WhichDir):
    f=None
    if WhichDir==1:
        saveLocal = 'fig cover AL1/' + str(n) + 'x' + str(m)
        if whichFile==1:
            f = open('E:/Desktop/project/fig/' + saveLocal + '/time.txt', "r")
        elif whichFile==2:
            f = open('E:/Desktop/project/fig/' + saveLocal + '/unitNum.txt', "r")
    elif WhichDir==2:
        saveLocal = 'fig cover AL2/' + str(n) + 'x' + str(m)
        if whichFile==1:
            f = open('E:/Desktop/project/fig/' + saveLocal + '/time.txt', "r")
        elif whichFile==2:
            f = open('E:/Desktop/project/fig/' + saveLocal + '/unitNum.txt', "r")
    elif WhichDir==3:
        f = open('E:/Desktop/project/fig/' + 'fig origin/' + str(n) + 'x' + str(m) + '/NumOfP.txt', "r")
    context = f.read()
    temp1=[]
    f.close()
    temp= context.split()
    print(len(temp))
    for i in range(0,len(temp)):
        x = temp[i][1:-1]
        temp1.append(x)
    return temp1#这时候列表的index就是该数据在原数据集的序号

# 将列表形式转化为字典形式，将数据的序号和其数值关联
def saveAsDectionary(temp1):
    temp2={}
    for i in range(0,len(temp1)):
        z = temp1[i].split(',')
        z0=float(z[0])
        z1=int(z[1])
        temp2[z1]=z0
    # for i in range(0,len(temp)):
    #     print(temp2[i])
    return temp2


# 将一个字典按照value降序排列转化为一个列表
def SortTheDataAndList(temp2):
    temp = sorted(temp2.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    return temp

# 计算数据和的其平均值，并筛选数据,temp1是数据值的列表形式，temp2是数据字典形式
# 并返回一个存有筛选后的点的序号的列表
def TheMeanOfdataAndPickup(temp2,NumOfPoint=500):
    temp1 = list(temp2.values())
    average = np.mean(temp1)
    DvalueWithAver = {}
    for i in range(0,len(temp1)):
        DvalueWithAver[i]=(abs(temp1[i]-average)) #将差值和序号对应
    # sorted(DvalueWithAver.values())#对差值排序
    temp = SortTheDataAndList(DvalueWithAver)
    #range的第二参数表示筛选的点的个数，如100就是去掉偏差过大的100个点
    for i in range(0,NumOfPoint):
        del temp[0]
    temp3=[]
    for item in temp:
        temp3.append(item[0])
    return temp3

# 根据筛选的序号列表，重新使用dictionary去存储
def createNewDicWithIndexList(OriginDic,IndexList):
    temp={}
    for item in IndexList:
        if OriginDic[item] != None:
            temp[item]=OriginDic[item]
    return temp

#画出散点图 筛选点后的图,temp2是数据字典，所有数据的
# DataIndexList为筛选后的数据序号列表
def DrawScatter(temp2,penColor,DataIndexList=None):
    color=["#6699cc","#ff1212","#00FF00"]#颜色分别为blue画time,red画unit个数,lime
    TheColorOfPen = color[penColor]
    if DataIndexList  != None:
        for item in DataIndexList:
            if temp2[item]!= None:
                plt.scatter(item, temp2[item], s=20, c=TheColorOfPen, marker='o')
    else:
        for i in range(0, len(temp2)):
            if temp2[i] != None:
                plt.scatter(i, temp2[i], s=20, c=TheColorOfPen, marker='o')


#画出柱状图,temp2是数据字典，所有数据的
# temp3为筛选后的数据序号列表,SizeOfData表示数据是哪个规模的,10x10就是1,20x20为2
def DrawBar(temp2,temp3,SizeOfData):
    temp1=[]
    for item in temp3:
        if temp2[item]!= None:
            temp1.append(temp2[item])
    average = np.mean(temp1)#计算筛选后的平均数
    # plt.bar(SizeOfData,average,facecolor='#9999ff',edgecolor='white')#蓝色
    # plt.bar(SizeOfData, average, facecolor='#ff9999', edgecolor='white')#红色，画unit个数
    plt.bar(SizeOfData, average, facecolor='#99ff99', edgecolor='white')  #green
    # plt.text(SizeOfData,average+0.005,'%.4f'%average,ha='center',va='bottom',size=20)
    plt.text(SizeOfData, average + 0.5, '%.0f' % average, ha='center', va='bottom', size=20)

# 读取文件后，筛选数据，求得平均值后，画出柱状图
def invokeTheFuncion(n,m,whichFile,Whichal):
    temp2 = readFileAndSaveAsDection(n, m, whichFile, Whichal)
    temp3 = TheMeanOfdataAndPickup(temp2)
    SizeOfData=(n/10)
    DrawBar(temp2, temp3, SizeOfData)

# 读取文件后，原数据保存为字典
#调用之前的方法
def readFileAndSaveAsDection(n,m,whichFile,Whichal):
    temp1 = readFile(n, m,whichFile,Whichal)#前面的为2为unitNum，后面为算法
    temp2 = saveAsDectionary(temp1)
    return temp2

# 根据点的个数来划分多边形,用字典来表示，key值是点的个数，value是数据的序号
def createDicWithPointKey(n,m):
    temp1 = readFile(n, m, 3, 3)
    temp2 = saveAsDectionary(temp1)
    temp = SortTheDataAndList(temp2)
    DictionOfResult={}
    for element in temp:
        index = element[1]
        DictionOfResult[index] = []
    for element in temp:
        index = element[1]
        DictionOfResult[index].append(element[0])
    return DictionOfResult

# 绘制折线图，根据多边形的点的个数，来计算一个平均复杂度增长图

# 从一种算法中读取所有组的相同类型文件
#类型有time，unitnum或者pointNum
def readSameFilesInAl(whichFile,whichDir):
    for element in RectangleSizeList:
        print(element)
        fig = plt.figure(figsize=(25, 15))
        OrigonDic = readFileAndSaveAsDection(element,element,whichFile,whichDir)#原始数据
        DataAfterScreen = TheMeanOfdataAndPickup(OrigonDic,NumOfPoint=1000)
        # TheDicAfterScreen = createNewDicWithIndexList(OrigonDic, DataAfterScreen)
        DrawScatter(OrigonDic,whichFile-1,DataAfterScreen)#画出散点图
        # # 设置坐标刻度间隔大小
        x_major_locator = plt.MultipleLocator(100)
        # y_major_locator=plt.MultipleLocator(5)
        plt.xlim(xmin=0)
        plt.ylim(ymin=0,ymax=TheMaxOfY[whichFile-1])#设置y轴最大值
        ax = plt.gca()
        ax.xaxis.set_major_locator(x_major_locator)
        # ax.yaxis.set_major_locator(y_major_locator)
        plt.tick_params(labelsize=30)
        plt.savefig(Savelocation1 + SaveWhichAl[whichDir-1] + str(element) + 'x' + str(element) + SaveASWhatName[whichFile-1] + '.png')
        # plt.show()
        plt.close(fig)

#打开或者创建一个excel file，并且写入10组的数据
def openAExcelFile(whichFile,whichDir,FileName):
    if os.path.exists(FileName):
        return
    workbook = xlsxwriter.Workbook(FileName)  # 创建一个Excel文件
    worksheet = workbook.add_worksheet()
    for element in RectangleSizeList:
        OrigonDic = readFileAndSaveAsDection(element, element, whichFile, whichDir)
        DataAfterScreen = TheMeanOfdataAndPickup(OrigonDic, NumOfPoint=1294)
        TheDicAfterScreen = createNewDicWithIndexList(OrigonDic, DataAfterScreen)
        writeDataToExcel(element, element, whichFile, whichDir, TheDicAfterScreen, worksheet)
    workbook.close()

#将数据写入excel：
def writeDataToExcel(n,m,whichFile,whichDir,DataList,worksheet):
    #接受的datalist为字典形式
    TheDicOfSizeAndColum={
        10:'A',20:'B',30:'C',40:'D',50:'E',60:'F',70:'G',80:'H',90:'I',100:'J',
    }
    AlgorithmName = [
        "al1",
        "al2",
        "origin",
    ]
    TheDataType = [
        'time',
        'unitNum',
        'vertexNum'
    ]
    title = [AlgorithmName[whichFile-1]+' '+str(n)+'x'+str(m)+' '+TheDataType[whichDir-1]]    #表格title
    worksheet.write_row(TheDicOfSizeAndColum[n]+'1',title)
    ValueList = list(DataList.values())
    tempList = ValueList+[np.mean(ValueList)]
    worksheet.write_column(TheDicOfSizeAndColum[n]+'2', tempList)

if __name__ == '__main__':
    n=RectangleSizeList[8]
    m=RectangleSizeList[8]
    # whichFile,1代表time，2代表unitNum，3代表NumOfp
    # whichDir，1代表算法1，2代表算法2，3代表原数据
    k = 1
    for i in range(1,4):
        if i == 3:
            whichFile = i
            whichDir = 3
            print(k)
            ExcelFileName = (Savelocation1 + SaveWhichAl[whichDir - 1] + SaveASWhatName[
                whichFile - 1] + '.xlsx')  # excel 文件存在哪里
            # readSameFilesInAl(whichFile, whichDir)
            openAExcelFile(whichFile, whichDir, ExcelFileName)
        else:
            for j in range(1,3):
                whichFile = i
                whichDir = j
                print(k)
                ExcelFileName = (Savelocation1 + SaveWhichAl[whichDir - 1] + SaveASWhatName[
                    whichFile - 1] + '.xlsx')#excel 文件存在哪里
                # readSameFilesInAl(whichFile, whichDir)
                openAExcelFile(whichFile, whichDir, ExcelFileName)  # 保存到excel文件中，方便绘图,包含文件读取功能
                k = k+1
    # readSameFilesInAl(whichFile, whichDir)
    print('finished--------')
    # OrigonDic = readFileAndSaveAsDection(n, m)#原始数据
    # temp3 = TheMeanOfdataAndPickup(OrigonDic)
    # for item in temp3:
    #     print(item)
    # temp = createDicWithPointKey(n,m)
    # x=[]
    # y=[]
    # for pointNum in temp:
    #     UnitNumOfsamePointNum =[]
    #     for index in temp[pointNum]:
    #         UnitNumOfsamePointNum.append(OrigonDic[index])
    #     average = np.mean(UnitNumOfsamePointNum)
    #     x.append(pointNum)
    #     y.append(average)
    # # plt.plot(x, y, '-', color='#99ff99', linewidth=2, zorder=1)
    # for i in range(0,len(x)):
    #     print(x[i],y[i])
    # print('-------------------------')
    # for item in temp:
    #     print(item,temp[item])
    # # plt.plot(x, y, '-', color='#9999ff', linewidth=2, zorder=1)
    # plt.plot(x, y, '-', color='#ff9999', linewidth=2, zorder=1)#红色
    # # DrawScatter(temp2,temp3)



    #     #算法1调用测试区域----
    #     # DrawCellList(test1.gridCellL)
    #     # DrawAlgorithm(findRectangle(test3),test3)
    #     # 算法1调用测试区域end----
    #     # -----------------------
    # # 算法2调用测试区域---------
    #     DrawConcaveSegmentList(test12.concaveSegmentL)
    #     DrawConvexSegmentList(test12.convexSegmentL)
    #     # 算法调用模块
    #     # newTemp = AlgorithmStage1(test12)
    #     # DrawRectangleList1(newTemp)
    #     # tempList = findUncoverConcaveSide(test12, newTemp)
    #     # DrawConvexSegmentList(tempList)
    #     # temp1 = findMaxRecOfNonCoverSide(tempList, test12)
    #     # DrawRectangleList1(temp1)
    #     # UnitList = AlgorithmStageOneAndTwo(test12)
    #     # DrawRectangleList1(UnitList)
    #     # uncoverCellList = AlgorithmStage3(UnitList, test12)
    #     # DrawAlgorithm1(UnitList, uncoverCellList, test12)
    #     # ---------------
    # # 算法2调用测试区域end--------

