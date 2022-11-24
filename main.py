import math
import os

import pyqtgraph as pg
import tifffile
from PyQt5 import QtCore, QtGui
from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
import numpy as np
import csv
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
        # self.globalBrainPath = './resources/SHG_Stack_Merge_20221021_092636188.tif'
        #
        # self.projectVideoPath = './resources/batch_processing_demo_data/002-1-AF-37.tif'
        # self.tifGlobalBrain = tifffile.imread(self.globalBrainPath)
        # self.tifProjectVideo = tifffile.imread(self.projectVideoPath)
        # self.iv1 = pg.ImageView()
        # iv2 = pg.ImageView()

        self.dataValue,self.dataJson=self.getCSVObject()
        print(self.dataValue)
        print(self.dataJson)
        x =['0-18','19-29','30-39','40-49','50-60']
        xdict = dict(enumerate(x))
        stringaxis = pg.AxisItem(orientation='bottom')
        stringaxis.setTicks([xdict.items()])
        # win = pg.PlotWidget(enableAutoRange=True,axisItems={'bottom': stringaxis})
        win = pg.GraphicsLayoutWidget(show=True, title="Basic plotting examples")
        # win = pg.PlotWidget(enableAutoRange=True)
        self.i = 0
        self.x = []  # x轴的值
        self.new_point_x = 0
        self.y = []  # y轴的值
        self.new_point_y = 0
        self.setMouseTracking(False)
        ## add scatter plots on top
        index=0
        p5 = win.addPlot(title="")
        for row in self.dataValue.values():
            # xvals = pg.pseudoScatter(data[i], spacing=0.4, bidir=True) * 0.2
            # print(data[i])
            self.scatter=p5.plot(x=row.get('age'), y=row.get('value'), pen=None, symbol='o', symbolBrush=pg.intColor(index, 6, maxValue=128))

            # self.scatter=win.plot(x=index, y=row.get('value'), pen=None, symbol='o', symbolBrush=pg.intColor(index, 6, maxValue=128))
            index+=1
        p5.setLabel('left', "ELCOR", units='F')
        p5.setLabel('bottom', "Age", units='I')
        # p5.setLogMode(x=True, y=False)


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
        self.imageName=""
        # self.cbox.currentTextChanged.connect(self.selectChange)
        self.pb_choose.clicked.connect(self.pb_choose_fcn)  # 选择文件路径
        self.verticalLayout_3.addWidget(win)
        self.setWindowTitle(SOFTWAREVERSION)
        self.setWindowIcon(QIcon(SOFTWAREICON))
    def loadFile(self):
        pass
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
    def getCSV(self):
        with open(r'resources/ELCOR/elcor_saaid_ratio.csv', encoding='UTF-8') as S1R:
            reader = csv.reader(S1R)
            for row in reader:
                pass
    def getCSVObject(self):

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
        with open(r'resources/ELCOR/elcor_saaid_ratio.csv', encoding='UTF-8') as S1R:
            reader = csv.reader(S1R)
            header = next(reader)
            for row in reader:
                rowjson = {
                    'id':row[0],
                    'value':row[1],
                    'age': row[3]
                }
                row1data=0
                if(self.is_number(row[1])):
                    row1data =row[1]

                datajson.append(rowjson)
                if(int(row[3])<19):
                    datadict.get('column1').get('name').append((row[0]))
                    datadict.get('column1').get('value').append(float(row1data))
                    datadict.get('column1').get('age').append(int(row[3]))
                elif(int(row[3])<29):
                    datadict.get('column2').get('name').append((row[0]))
                    datadict.get('column2').get('value').append(float(row1data))
                    datadict.get('column2').get('age').append(int(row[3]))
                elif (int(row[3])< 39):
                    datadict.get('column3').get('name').append((row[0]))
                    datadict.get('column3').get('value').append(float(row1data))
                    datadict.get('column3').get('age').append(int(row[3]))
                elif (int(row[3]) < 49):
                    datadict.get('column4').get('name').append((row[0]))
                    datadict.get('column4').get('value').append(float(row1data))
                    datadict.get('column4').get('age').append(int(row[3]))
                elif (int(row[3])< 61):
                    datadict.get('column5').get('name').append((row[0]))
                    datadict.get('column5').get('value').append(float(row1data))
                    datadict.get('column5').get('age').append(int(row[3]))
        return datadict,datajson
    def scatter_clicked(self, plot, points):
        index_val = points[0].index()
        print(index_val)
        pass

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
        self.imageName,values,age=self.getSingleData(point_x,point_y)
        self.selectLable.setText('编号：'+self.imageName+' 年龄：'+str(age)+' 值：'+str(format(values, '.3f')))
        pathfileAF=self.find('./resources/batch_processing_demo_data',self.imageName+'-AF')
        pathfileSHG= self.find('./resources/batch_processing_demo_data',self.imageName + '-SHG' )
        if (len(pathfileAF) > 0):
            self.showImageAF(pathfileAF[0], pathfileAF[0])
        else:
            for i in range(self.VLBotoom_AF.count()):
                self.VLBotoom_AF.itemAt(i).widget().deleteLater()
            for i in range(self.verticalLayout_AF.count()):
                self.verticalLayout_AF.itemAt(i).widget().deleteLater()
        if(len(pathfileSHG)>0):
            self.showImageSHG(pathfileSHG[0],pathfileSHG[0])
        else:
            for i in range(self.VLBotoom_SHG.count()):
                self.VLBotoom_SHG.itemAt(i).widget().deleteLater()
            for i in range(self.verticalLayout_SHG.count()):
                self.verticalLayout_SHG.itemAt(i).widget().deleteLater()


    def getSingleData(self,point_x, point_y):
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
        for i in range(self.VLBotoom_AF.count()):
            self.VLBotoom_AF.itemAt(i).widget().deleteLater()
        for i in range(self.verticalLayout_AF.count()):
            self.verticalLayout_AF.itemAt(i).widget().deleteLater()
        tifGlobalBrain = tifffile.imread(path1)
        tifProjectVideo = tifffile.imread(path2)
        iv1 = pg.ImageView()
        iv2 = pg.ImageView()
        iv1.setImage(tifGlobalBrain)
        iv2.setImage(tifProjectVideo)
        iv1.ui.menuBtn.setVisible(False)
        iv1.ui.roiBtn.setVisible(False)
        iv2.ui.menuBtn.setVisible(False)
        iv2.ui.roiBtn.setVisible(False)
        # iv2.setImage(self.tifProjectVideo , axes={'t': 0, 'x': 2, 'y': 1})
        self.verticalLayout_AF.addWidget(iv1)
        self.VLBotoom_AF.addWidget(iv2)
    def showImageSHG(self,path1,path2):
        for i in range(self.VLBotoom_SHG.count()):
            self.VLBotoom_SHG.itemAt(i).widget().deleteLater()
        for i in range(self.verticalLayout_SHG.count()):
            self.verticalLayout_SHG.itemAt(i).widget().deleteLater()
        tifGlobalBrain = tifffile.imread(path1)
        tifProjectVideo = tifffile.imread(path2)
        iv1 = pg.ImageView()
        iv2 = pg.ImageView()
        iv1.setImage(tifGlobalBrain)
        iv2.setImage(tifProjectVideo)
        iv1.ui.menuBtn.setVisible(False)
        iv1.ui.roiBtn.setVisible(False)
        iv2.ui.menuBtn.setVisible(False)
        iv2.ui.roiBtn.setVisible(False)
        # iv2.setImage(self.tifProjectVideo , axes={'t': 0, 'x': 2, 'y': 1})
        self.verticalLayout_SHG.addWidget(iv1)
        self.VLBotoom_SHG.addWidget(iv2)
    def errorMsg(self,msg):
        loading_msg_box = QMessageBox()
        loading_msg_box.setWindowTitle('错误')
        loading_msg_box.setIcon(QMessageBox.Critical)
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
        folder_path = QFileDialog.getExistingDirectory(self.ui, "选择文件夹")
        print(folder_path)
        self.ui.txt_path.setText(folder_path)
        self.pb_loading_fcn();

    def pb_loading_fcn(self):
        # 1
        # 用户输入 新建的项目的保存地址：project_xss_large/
        project_dir = self.txt_path.toPlainText()
        # 2, 3
        try:
            # 依次调用下面的
            self.dataBase = DataModule(project_dir)
        except Exception as e:
            # 访问异常的错误编号和详细信息
            # print(e.args)
            # print(repr(e))
            print(str(e))
            self.msgBox("加载项目失败",icon=QMessageBox.Critical)
            self.dataBase = None
            return
        # 4
        # 成功加载项目
        self.msgBox("加载项目成功",title='成功' ,icon=QMessageBox.Information)
        # 设置comboBox_Y轴的下拉框
       # self.setYItems()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    ui = BMAEWindow()

    ui.show()
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()