import math
import os
import random

import pyqtgraph as pg
import tifffile
from PyQt5 import QtCore, QtGui
from PyQt5 import uic
from PyQt5.Qt import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
import numpy as np
import pandas as pd
from PIL import Image
SOFTWAREVERSION = r'Observers Tool'
SOFTWAREICON = r'./resources/jrk.png'
SOFTWARECOPYRIGHT = r' 2022'
SOFTWAREAUTHOR = r'miaopeng'
WELCOMEMESSAGE = 'Welcom to use ' + SOFTWAREVERSION + "!"


class BMAEWindow(QMainWindow):
    lastOpenPath = r'./resources/'
    imgTIF = None
    def __init__(self):
        super(BMAEWindow, self).__init__()#调用父类的构造函数
        uic.loadUi(r'./Observer.ui', self)
        self.setWindowFlags(QtCore.Qt.MSWindowsFixedSizeDialogHint)
        self.setFocusPolicy(Qt.StrongFocus)
        self.currentdata={
            'id':"",
            'type':'',
            'value':0,
            'age':0
        }
        image = Image.open('./resources/ELCOR/404.png')
        self.nonoimgdata=np.array(image)

        self.iv1 = pg.ImageView()
        self.iv2 = pg.ImageView()
        self.iv3 = pg.ImageView()
        self.iv4 = pg.ImageView()
        self.iv1.ui.histogram.hide()
        self.iv1.ui.menuBtn.setVisible(False)
        self.iv1.ui.roiBtn.setVisible(False)
        self.iv2.ui.histogram.hide()
        self.iv2.ui.menuBtn.setVisible(False)
        self.iv2.ui.roiBtn.setVisible(False)

        self.iv3.ui.histogram.hide()
        self.iv3.ui.menuBtn.setVisible(False)
        self.iv3.ui.roiBtn.setVisible(False)
        self.iv4.ui.histogram.hide()
        self.iv4.ui.menuBtn.setVisible(False)
        self.iv4.ui.roiBtn.setVisible(False)
        self.verticalLayout_AF.addWidget(self.iv1)
        self.VLBotoom_AF.addWidget(self.iv2)
        self.verticalLayout_SHG.addWidget(self.iv3)
        self.VLBotoom_SHG.addWidget(self.iv4)
        self.pb_choose.clicked.connect(self.pb_choose_fcn)  # 选择文件路径
        self.grabKeyboard()
        self.setWindowTitle(SOFTWAREVERSION)
        self.setWindowIcon(QIcon(SOFTWAREICON))
    def ResetloadFile(self,path):
        for i in range(self.verticalLayout_3.count()):
            self.verticalLayout_3.itemAt(i).widget().deleteLater()
        self.dataValue, self.dataJson = self.getCSVObject(path)
        self.win = pg.GraphicsLayoutWidget(show=True, title="Basic plotting examples")
        self.i = 0
        self.x = []  # x轴的值
        self.y = []  # y轴的值
        self.setMouseTracking(False)
        ## add scatter plots on top
        index = 0
        self.p5 = self.win.addPlot(title="")
        for row in self.dataValue.values():
            # xvals = pg.pseudoScatter(data[i], spacing=0.4, bidir=True) * 0.2
            # print(data[i])
            self.scatter = self.p5.plot(x=row.get('age'), y=row.get('value'), pen=None, symbol='o',
                                   symbolBrush=pg.intColor(index+1, 6, maxValue=128))

            # self.scatter=win.plot(x=index, y=row.get('value'), pen=None, symbol='o', symbolBrush=pg.intColor(index, 6, maxValue=128))
            index += 1
        self.p5.setLabel('left', "ELCOR", units='F')
        self.p5.setLabel('bottom', "Age", units='I')
        # p5.setLogMode(x=True, y=False)

        self.scatter.scene().sigMouseMoved.connect(self.mouseover)
        self.scatter.scene().sigMouseClicked.connect(self.mouse_clicked)

        self.imageName = ""

        self.verticalLayout_3.addWidget(self.win)
    def loadFile(self,path):
        self.dataValue, self.dataJson = self.getCSVObject(path)

        print(self.dataValue)
        print(self.dataJson)
        x = ['0-18', '19-29', '30-39', '40-49', '50-60']
        xdict = dict(enumerate(x))
        stringaxis = pg.AxisItem(orientation='bottom')
        stringaxis.setTicks([xdict.items()])
        # win = pg.PlotWidget(enableAutoRange=True,axisItems={'bottom': stringaxis})
        self.win = pg.GraphicsLayoutWidget(show=True, title="Basic plotting examples")
        # win = pg.PlotWidget(enableAutoRange=True)
        self.i = 0
        self.x = []  # x轴的值
        self.new_point_x = 0
        self.y = []  # y轴的值
        self.new_point_y = 0
        self.setMouseTracking(False)
        ## add scatter plots on top
        index = 0
        self.p5 = self.win.addPlot(title="")
        for row in self.dataValue.values():
            # xvals = pg.pseudoScatter(data[i], spacing=0.4, bidir=True) * 0.2
            # print(data[i])
            self.scatter = self.p5.plot(x=row.get('age'), y=row.get('value'), pen=None, symbol='o',
                                   symbolBrush=pg.intColor(index+1, 6, maxValue=128))

            # self.scatter=win.plot(x=index, y=row.get('value'), pen=None, symbol='o', symbolBrush=pg.intColor(index, 6, maxValue=128))
            index += 1
        self.p5.setLabel('left', "ELCOR", units='F')
        self.p5.setLabel('bottom', "Age", units='I')
        # p5.setLogMode(x=True, y=False)
        firstnode=self.dataJson[0]
        self.resetDrawGrapher(firstnode.get('id'), firstnode.get('value'), firstnode.get('age'))
        self.scatter.scene().sigMouseMoved.connect(self.mouseover)
        self.scatter.scene().sigMouseClicked.connect(self.mouse_clicked)
        ## Make error bars
        # err = pg.ErrorBarItem(x= np.arange(4), y=[0.021752937, 0.017515702, 0.042893175, 0.127207753], height=data.std(axis=1), beam=0.5,
        #                       pen={'color': 'w', 'width': 2})
        # win.addItem(err)
        # print(data.mean(axis=1))
        # print(data.std(axis=1))

        # 捕捉鼠标单击事件
        # self.iv1.setImage(self.tifGlobalBrain)
        # iv2.setImage(self.tifProjectVideo)
        # iv1.ui.menuBtn.setVisible(False)
        # iv1.ui.roiBtn.setVisible(False)
        # iv2.ui.menuBtn.setVisible(False)
        # iv2.ui.roiBtn.setVisible(False)
        # # iv2.setImage(self.tifProjectVideo , axes={'t': 0, 'x': 2, 'y': 1})
        # self.iv1.timeLine.sigPositionChanged.connect(self.slotIndexChanged)
        # self.gViewCellVideo.getHistogramWidget().setVisible(False)#保留调节窗宽窗位窗口
        # self.VLBotoom.addWidget(self.iv1)
        # self.verticalLayout_2.addWidget(iv2)
        # self.qCheckBox[0].stateChanged.connect(self.All)
        self.imageName = ""
        # self.cbox.currentTextChanged.connect(self.selectChange)

        self.verticalLayout_3.addWidget(self.win)
    def selectChange(self):
        if self.cbox.currentIndex() == 0:
            print(self.cbox.currentText())
        else:
            print(self.cbox.currentText())
        if(self.imageName!=''):
            name = self.imageName + '-' + self.cbox.currentText()
            print(name)
            pathfile = self.find('./resources/batch_processing_demo_data', name)
            print(pathfile)
            if (len(pathfile) > 0):
                self.showImage(pathfile[0], pathfile[0])
            else:
                self.errorMsg('未找到对应文件')


    def slotIndexChanged(self):
        (index, time) = self.iv1.timeIndex(self.iv1.timeLine)
        self.iv1.setCurrentIndex(index)
        img=self.tifGlobalBrain[index,:,:]
        iv2 = pg.ImageView()
        iv2.setImage(img)
        for i in range(self.verticalLayout_2.count()):
            self.verticalLayout_2.itemAt(i).widget().deleteLater()
        self.verticalLayout_2.addWidget(iv2)
        print(index,time)
        # self.statusBar().showMessage("当前播放的是：" + str(index) +"帧")
    # def getCSV(self):
    #     with open(r'resources/ELCOR/elcor_saaid_ratio.csv', encoding='UTF-8') as S1R:
    #         reader = csv.reader(S1R)
    #         for row in reader:
    #             pass
    def getCSVObject(self,path):

        datajson=[]
        datadict = {
            'column1':{
                'name' :[],
                'age':[],
                'value': []
            },
            'column2': {
                'name': [],
                'age':[],
                'value': []
            },
            'column3': {
                'name': [],
                'age': [],
                'value': []
            },
            'column4': {
                'name': [],
                'age': [],
                'value': []
            },
            'column5': {
                'name': [],
                'age': [],
                'value': []
            }
        }
        # data = pd.read_csv(path, header=None)
        # data.sort_values(by='age')
        # # 读取
        # csv_result = pd.read_csv(path, usecols=head_row_list)
        row_list = self.csv_file_read(path)
        for row in row_list:
            if(row[3]==1):
                row1data = 0
                if (self.is_number(row[1])):
                    row1data = row[1]
                rowjson = {
                    'id': row[0],
                    'value': float(row1data),
                    'age': int(row[2])
                }
                datajson.append(rowjson)
                if (int(row[2]) < 19):
                    datadict.get('column1').get('name').append((row[0]))
                    datadict.get('column1').get('value').append(float(row1data))
                    datadict.get('column1').get('age').append(int(row[2]))
                elif (int(row[2]) < 29):
                    datadict.get('column2').get('name').append((row[0]))
                    datadict.get('column2').get('value').append(float(row1data))
                    datadict.get('column2').get('age').append(int(row[2]))
                elif (int(row[2]) < 39):
                    datadict.get('column3').get('name').append((row[0]))
                    datadict.get('column3').get('value').append(float(row1data))
                    datadict.get('column3').get('age').append(int(row[2]))
                elif (int(row[2]) < 49):
                    datadict.get('column4').get('name').append((row[0]))
                    datadict.get('column4').get('value').append(float(row1data))
                    datadict.get('column4').get('age').append(int(row[2]))
                elif (int(row[2]) < 61):
                    datadict.get('column5').get('name').append((row[0]))
                    datadict.get('column5').get('value').append(float(row1data))
                    datadict.get('column5').get('age').append(int(row[2]))
        return datadict,datajson
    def scatter_clicked(self, plot, points):
        index_val = points[0].index()
        print(index_val)
        pass


    def csv_file_read(self,path):
        # 读取表头
        head_row = pd.read_csv(path, nrows=0)
        # 表头列转为 list
        head_row_list = list(head_row)
        # 读取, usecols=head_row_list
        csv_result = pd.read_csv(path)
        csv_result = csv_result.sort_values(by=['Age', 'ELCOR_SAAID_RATIO'], ascending=[True,False])
        csv_result.drop_duplicates(subset=['ID'], keep ='first', inplace = True)
        row_list = csv_result.values.tolist()
        # print(f"行读取结果：{row_list}")
        # col_obj = csv_result.T
        # col_list = col_obj.values.tolist()
        # print(f"行转列读取结果：{col_list}")
        # csv_resultAge = pd.read_csv(r'F:/pythonwork/PyObserverTool/resources/ELCOR/id_age.csv')
        # csv_resultAge.drop_duplicates(subset=['ID'], keep='first', inplace=True)
        # output3 = pd.merge(csv_result, csv_resultAge, on='ID', how='inner')
        # print(output3)
        return row_list

    def getDownUpOtherData(self,direct):
        current=self.currentdata
        currentid=current.get('id')
        currentage = current.get('age')
        index=0

        for x in self.dataJson:
            if x.get('id') == currentid:
                index=(self.dataJson.index(x))
                print(index)
        if(direct=='down'):
            index=index+1
        elif(direct=='up'):
            index=index-1

        if(len(self.dataJson)<=index):
            index=0
        if (index<0):
            index = len(self.dataJson)-1
        nextdata=self.dataJson[index]
        if(nextdata.get('age')==currentage):
            self.currentdata.update({'id': nextdata.get('id')})
            self.currentdata.update({'value': nextdata.get('value')})
            self.currentdata.update({'age': nextdata.get('age')})
        else:
            return current

        return nextdata

    def getLeftRightOtherData(self, direct):
        current = self.currentdata
        currentid = current.get('id')
        currentage = current.get('age')
        currentvalue = current.get('value')
        index=0

        for x in self.dataJson:
            if x.get('id') ==currentid:
                index = (self.dataJson.index(x))
                print(index)
        if (direct == 'right'):
            index = index + 1
        elif (direct == 'left'):
            index = index - 1

        if (len(self.dataJson) <= index):
            index = 0
        if (index < 0):
            index = len(self.dataJson) - 1
        nextdata = self.dataJson[index]
        if (nextdata.get('age') == currentage):
           while nextdata.get('age') == currentage:
               if (direct == 'right'):
                   index = index + 1
               elif (direct == 'left'):
                   index = index - 1
               if (len(self.dataJson) <= index):
                   index = 0
               if (index < 0):
                   index = len(self.dataJson) - 1
               nextdata = self.dataJson[index]
            #查询年龄相同的数据
           nextdata=self.getAgeSameNode(nextdata.get('age'),currentvalue)

        else:
            nextdata = self.getAgeSameNode(nextdata.get('age'), currentvalue)
            self.currentdata.update({'id': nextdata.get('id')})
            self.currentdata.update({'value': nextdata.get('value')})
            self.currentdata.update({'age': nextdata.get('age')})

        return nextdata
    def getAgeSameNode(self,Age,value):
        AgeArr=[]
        AgeValue=[]
        for x in self.dataJson:
            if x.get('age') == Age:
                AgeArr.append(x)
                AgeValue.append(x.get('value'))
        idx,v=self.find_nearest(AgeValue,value)
        return AgeArr[idx]
    # if contains(myList, lambda x: x.n == 3)  # True if any element has .n==3

    # do stuff
    # 重写键盘按下事件self.label.grabKeyboard()   #控件开始捕获键盘
    def keyPressEvent(self, event):
        # 如果按下xxx则xxx
        pass
        event.ignore()
        if event.key() == Qt.Key_Up:
            print('Key_Up')
            nextdata=self.getDownUpOtherData('up')
            print(nextdata)
            self.resetDrawGrapher(nextdata.get('id'), nextdata.get('value'), nextdata.get('age'))
        # 组合键
        elif (event.key() == Qt.Key_Down):
            print('Key_Down')
            nextdata=self.getDownUpOtherData('down')
            print(nextdata)
            self.resetDrawGrapher(nextdata.get('id'), nextdata.get('value'), nextdata.get('age'))
        elif (event.key() == Qt.Key_Left):
            print('Key_Left')
            nextdata=self.getLeftRightOtherData('left')
            print(nextdata)
            self.resetDrawGrapher(nextdata.get('id'), nextdata.get('value'), nextdata.get('age'))
        elif (event.key() == Qt.Key_Right):
            print('Key_Right')
            nextdata=self.getLeftRightOtherData('right')
            print(nextdata)
            self.resetDrawGrapher(nextdata.get('id'), nextdata.get('value'), nextdata.get('age'))
        else:
            QWidget.keyPressEvent(self, event)


    # 鼠标移动事件，用于获取精确坐标（好像鼠标单击的坐标不准确）
    def mouseover(self, pos):
        # 参数pos 是像素坐标，需要 转化为  刻度坐标
        act_pos = self.scatter.mapFromScene(pos)
        if type(act_pos) != QtCore.QPointF:
            return
        # print("over_1:",act_pos.x(), act_pos.y())
        self.new_point_x = act_pos.x()
        self.new_point_y = act_pos.y()

        # 鼠标单击事件，用于鼠标单击后事件的处理，包括：
        # 1）添加新坐标
    def mouse_clicked(self, event):
        self.x.append(self.new_point_x)
        self.y.append(self.new_point_y)
        point_x=self.new_point_x
        point_y=self.new_point_y
        print(point_x, point_y)
        project_dir = self.txt_path.text()
        if project_dir == '':
            return
        self.ResetloadFile(project_dir)
        id,values,age=self.getSingleData(point_x,point_y)
        if(id!=''):
            self.resetDrawGrapher(id, values, age)
        else:
            print('查找数据出错')

    def resetDrawGrapher(self,id, values, age):
        project_dir = self.txt_path.text()
        if project_dir == '':
            return
        self.ResetloadFile(project_dir)
        self.currentdata.update({'id': id})
        self.currentdata.update({'value': values})
        self.currentdata.update({'age': age})
        type = self.currentdata.get('type')
        self.p5.plot([age], [values], pen=(200, 200, 200), symbolBrush=(255, 0, 0), symbolPen='w')
        pathfileAF = self.find('./resources/' + type + '/data', id + '-AF')
        pathfileSHG = self.find('./resources/' + type + '/data', id + '-SHG')
        pathfileAF3 = self.find('./resources/' + type + '/data3d', id + '-AF')
        pathfileSHG3 = self.find('./resources/' + type + '/data3d', id + '-SHG')
        arrrange=['010-1','003-1','010-2','005-2','011-1']
        d3index=(arrrange[random.randint(0,3)])
        if (len(pathfileAF3) ==0):
            pathfileAF3 = self.find('./resources/' + type + '/data3d', d3index+'-AF')
        if (len(pathfileSHG3) == 0):
            pathfileSHG3 = self.find('./resources/' + type + '/data3d',d3index+'-SHG')
        Nonestr=''
        print(pathfileAF,pathfileSHG)
        print(pathfileAF3,pathfileSHG3)
        try:
            if (len(pathfileAF) > 0 and len(pathfileAF3) > 0):
                print('AF')
                self.showImageAF(pathfileAF[0], pathfileAF3[0])
                self.labelOne.setText('AF')
            else:
                Nonestr = '（未找到对应图像）'
                self.notFindImg('AF')
                # for i in range(self.VLBotoom_AF.count()):
                #     self.VLBotoom_AF.itemAt(i).widget().deleteLater()
                # for i in range(self.verticalLayout_AF.count()):
                #     self.verticalLayout_AF.itemAt(i).widget().deleteLater()
            if (len(pathfileSHG) > 0 and len(pathfileSHG3) > 0):
                print('SHG')
                self.showImageSHG(pathfileSHG[0], pathfileSHG3[0])
                self.labeltwo.setText('SHG')
            else:
                self.notFindImg('SHG')
            self.selectLable.setText(' 编号：' + id + '  年龄:' + str(age) + '  值：' + str(format(values, '.3f')))
            dir_path = os.path.dirname(project_dir)
            if Nonestr != '':
                dir_path = Nonestr
            else:
                pass
                # dir_path = dir_path + '/data'
            # self.selectLable_2.setText(dir_path)
        except Exception as e:
            print(e)
        finally:
            print('最后执行')



    def getSingleData(self,point_x, point_y):
        print(point_x,point_y)
        if (point_x < 19.1):
            name1 = self.dataValue.get('column1').get('name')
            value1 = self.dataValue.get('column1').get('value')
            age1 = self.dataValue.get('column1').get('age')
            index1, values = self.find_nearest(value1, point_y)
            print(value1)
            print(index1, values)
            return name1[index1],values,age1[index1]
        elif (point_x < 29.1):
            name1 = self.dataValue.get('column2').get('name')
            value1 = self.dataValue.get('column2').get('value')
            age1 = self.dataValue.get('column2').get('age')
            index1, values = self.find_nearest(value1, point_y)
            print(value1)
            print(index1, values)
            return name1[index1],values,age1[index1]
        elif (point_x < 39.1):
            name1 = self.dataValue.get('column3').get('name')
            value1 = self.dataValue.get('column3').get('value')
            age1 = self.dataValue.get('column3').get('age')
            index1, values = self.find_nearest(value1, point_y)
            print(value1)
            print(index1, values)
            return name1[index1],values,age1[index1]
        elif (point_x < 49.1):
            name1 = self.dataValue.get('column4').get('name')
            value1 = self.dataValue.get('column4').get('value')
            age1 = self.dataValue.get('column4').get('age')
            index1, values = self.find_nearest(value1, point_y)
            print(value1)
            print(index1, values)
            return name1[index1],values,age1[index1]
        elif (point_x < 61.1):
            name1 = self.dataValue.get('column5').get('name')
            value1 = self.dataValue.get('column5').get('value')
            age1 = self.dataValue.get('column5').get('age')
            index1, values = self.find_nearest(value1, point_y)
            print(value1)
            print(index1, values)
            return name1[index1],values,age1[index1]
        else:
            print('error')
            return 0,0,0
    def find_nearest(self,array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return idx,array[idx]

    def find(self,dir, name):
        # print(dir)
        pathArr=[]
        for i in [x for x in os.listdir(dir) if
                  os.path.isfile(os.path.join(dir, x)) and os.path.splitext(x)[0].startswith(name)]:
            path=(os.path.join(dir, i))
            if(path!='None'):
                pathArr.append(path.replace('\\','/'))
        return pathArr
    def showImageAF(self,path1,path2):
        # for i in range(self.VLBotoom_AF.count()):
        #     self.VLBotoom_AF.itemAt(i).widget().deleteLater()
        # for i in range(self.verticalLayout_AF.count()):
        #     self.verticalLayout_AF.itemAt(i).widget().deleteLater()

        tifGlobalBrain = tifffile.imread(path1)
        tifProjectVideo = tifffile.imread(path2)

        self.iv1.setImage(tifGlobalBrain)
        self.iv1.ui.menuBtn.setVisible(False)
        self.iv1.ui.roiBtn.setVisible(False)
        self.iv1.ui.histogram.show()

        self.iv2.setImage(tifProjectVideo)
        self.iv2.ui.menuBtn.setVisible(False)
        self.iv2.ui.roiBtn.setVisible(False)
        self.iv2.ui.histogram.show()
        # iv2.setImage(tifProjectVideo , axes={'t': 0, 'x': 2, 'y': 1})

    def notFindImg(self,pos):
        # for i in range(self.VLBotoom_AF.count()):
        #     self.VLBotoom_AF.itemAt(i).widget().deleteLater()
        # for i in range(self.verticalLayout_AF.count()):
        #     self.verticalLayout_AF.itemAt(i).widget().deleteLater()

        # 如果之前未设置显示选项以行为主，这里需要对显示图像进行转置pos
        if pos=='AF':
            self.iv1.setImage(self.nonoimgdata)
            self.iv2.setImage(self.nonoimgdata)
            self.iv1.ui.histogram.hide()
            self.iv2.ui.histogram.hide()
        else:
            self.iv3.setImage(self.nonoimgdata)
            self.iv4.setImage(self.nonoimgdata)
            self.iv3.ui.histogram.hide()
            self.iv4.ui.histogram.hide()

    def showImageSHG(self,path1,path2):
        # for i in range(self.VLBotoom_SHG.count()):
        #     self.VLBotoom_SHG.itemAt(i).widget().deleteLater()
        # for i in range(self.verticalLayout_SHG.count()):
        #     self.verticalLayout_SHG.itemAt(i).widget().deleteLater()
        tifGlobalBrain = tifffile.imread(path1)
        tifProjectVideo = tifffile.imread(path2)
        self.iv3.setImage(tifGlobalBrain)
        self.iv4.setImage(tifProjectVideo)
        self.iv3.ui.menuBtn.setVisible(False)
        self.iv3.ui.roiBtn.setVisible(False)
        self.iv3.ui.histogram.show()
        self.iv4.ui.menuBtn.setVisible(False)
        self.iv4.ui.roiBtn.setVisible(False)
        self.iv4.ui.histogram.show()
        # iv2.setImage(self.tifProjectVideo , axes={'t': 0, 'x': 2, 'y': 1})

    def errorMsg(self,msg):
        loading_msg_box = QMessageBox()
        loading_msg_box.setWindowTitle('错误')
        loading_msg_box.setIcon(QMessageBox.Critical)
        loading_msg_box.setText(msg)
        # create_msg_box.(QMessageBox.Retry | QMessageBox.Abort | QMessageBox.Ignore)
        loading_msg_box.addButton('确定', QMessageBox.YesRole)
        loading_msg_box.exec()

    def msgBox(self,msg, title,icon):
        loading_msg_box = QMessageBox()
        loading_msg_box.setWindowTitle(title)
        loading_msg_box.setIcon(icon)
        loading_msg_box.setText(msg)
        # create_msg_box.(QMessageBox.Retry | QMessageBox.Abort | QMessageBox.Ignore)
        loading_msg_box.addButton('确定', QMessageBox.YesRole)
        loading_msg_box.exec()

    def is_number(self,s):

        try:
            ss= float(s)
            if math.isnan(ss):
                return False
            return True
        except ValueError:
            pass

        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass

        return False


    def pb_choose_fcn(self):
        """choose file path"""
        # 定义文件对话框类
        folder_path = QFileDialog.getOpenFileName(self, "选择文件夹")
        print(folder_path)
        self.txt_path.setText(folder_path[0])
        self.pb_loading_fcn();

    def pb_loading_fcn(self):
        # 1
        # 用户输入 新建的项目的保存地址：project_xss_large/
        project_dir = self.txt_path.text()
        if project_dir=='':
            return
        # 2, 3
        try:
            # 依次调用下面的
            dir_path = os.path.dirname(project_dir)
            dir_pathlist= os.path.split(dir_path)
            print(dir_pathlist)
            self.currentdata.update({'type':dir_pathlist[1]})
            self.loadFile(project_dir)
        except Exception as e:
            print(str(e))
            self.msgBox("数据加载失败",title='错误',icon=QMessageBox.Critical)
            return
        # 4
        # 成功加载项目
        # self.msgBox("加载项目成功",title='成功' ,icon=QMessageBox.Information)
    def mergeCsv(self,path1,path2):
        data1 = pd.read_csv(path1)
        data2 = pd.read_csv(path2)
        # data1, data2: 用于合并的数据帧。
        # how: {‘left’, ‘right’, ‘outer’, ‘inner’}，默认’inner’
        # on：label
        # 或
        # list
        # using merge function by setting how='right'
        output3 = pd.merge(data1, data2,on='ID', how='inner')


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    ui = BMAEWindow()

    ui.show()
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()