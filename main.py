#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    :
# @Author  :
# @Site    :
# @File    : main.py.py
# @Software: PyCharm

# -*- coding: utf-8 -*-

import sys
import tcp_Logic
import udp_Logic
# import webengine
import tcp_udp_ui
import PyQt5.sip
from PySide2 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy, \
    QLabel, QPushButton, QFileDialog, QMessageBox
from netAssitui import Ui_NetAssist
from webengine import Child
# from QCandyUi import CandyWindow
# import qdarkstyle
from PyQt5.QtCore import QTimer, QFile

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtUiTools import QUiLoader

import os


class PyQt5_Netassist(QMainWindow, tcp_Logic.TcpLogic,
                      udp_Logic.UdpLogic, tcp_udp_ui.Tcp_ucpUi, Ui_NetAssist):
    def __init__(self):
        # Python3中的继承只用一个super()就可以了，继承后初始化父类的属性

        super(PyQt5_Netassist, self).__init__()
        self.setupUi(self)
        self.path = None
        self.working = False
        self.newline.setChecked(1)
        self.remoteip_lbl.hide()
        self.remoteip_text.hide()
        self.remoteport_text.hide()
        self.remoteport_lbl.hide()
        self.init()
        self.custom_connect()
        self.init_statusbar()
        self.open_btn.setToolTip("Verbindung öffnen")

    def init(self):

        #
        # #添加webengine
        # self.plotButton.clicked.connect(self.show_ialweb)

        # 打印选择的协议类型编号
        self.prot_box.currentTextChanged.connect(self.proto_imf)
        # 对open_btn按下进行判断：TCPserver or TCPClient
        self.open_btn.clicked.connect(self.click_select_open)
        # 关闭socket
        self.close_btn.clicked.connect(self.click_select_close)
        # 按钮发送数据
        self.send_Btn.clicked.connect(self.data_send_select)
        # 文件发送按钮
        self.file_send_btn.clicked.connect(self.file_send_select)
        # 清空接收区显示
        self.clr_btn.clicked.connect(self.recv_dataclear)
        # 清空发送区显示
        self.clr_btn2.clicked.connect(self.send_dataclear)
        # 当标记Status改变时触发信号，recv2file的isCheckedStatus作为Status改变的参考
        self.recv2file.toggled.connect(self.rfilechoose)
        # 按下保存数据按钮，进行保存操作
        self.save_btn.clicked.connect(self.datasave2file)
        # 载入需要发送的文件
        self.file_load.toggled.connect(self.send_fileload)
        # 定时器启动检测
        self.Sendloop.toggled.connect(self.checktimer)
        # 发送校验位选择
        self.Sendcheck.toggled.connect(self.checksend_choose)


    def init_statusbar(self):
        # 设置statusbar所有控件自动延伸
        self.statusbar.setSizePolicy(QSizePolicy.Expanding,
                                     QSizePolicy.Expanding)
        # 设置status隐藏控制点（靠齐最右边）
        self.statusbar.setSizeGripEnabled(False)
        self.statusbar_dict['status'] = QLabel()
        self.statusbar_dict['status'].setText('Status：Ready')
        self.statusbar_dict['tx'] = QLabel()
        # self.statusbar_dict['space']=QSpacerItem(20,20,QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.statusbar_dict['tx'].setText('Anzahl senden：0')
        self.statusbar_dict['rx'] = QLabel()
        self.statusbar_dict['rx'].setText('Zählung erhalten：0')
        self.statusbar_dict['clear'] = QPushButton()
        self.statusbar_dict['clear'].setText('Löschen')
        self.statusbar_dict['clear'].setToolTip('Löschen die Zählung der Sendung und Erhaltung erhalten')
        self.statusbar_dict['clear'].pressed.connect(
            self.statusbar_clear_pressed)

        for i, w in enumerate(self.statusbar_dict.values()):
            if i != len(self.statusbar_dict) - 1:
                self.statusbar.addWidget(w, 20)
            else:
                # 最后一个控件不拉伸
                self.statusbar.addWidget(w)

    def statusbar_clear_pressed(self):
        self.statusbar_dict['tx'].setText('Anzahl senden：0')
        self.statusbar_dict['rx'].setText('Zählung erhalten：0')
        self.rx_count = 0
        self.tx_count = 0

    def checktimer(self):
        '''
        检测Timer是否需要开启
        :return:
        '''
        if self.Sendloop.isChecked():
            self.timer = QTimer(self)
            try:
                self.interval = int(self.loopinterval.text())
                if self.file_load.isChecked():
                    # 下面connect横线是pycharm的一个bug，不需理会
                    self.timer.timeout.connect(self.file_send_select)
                else:
                    # 下面connect横线是pycharm的一个bug，不需理会
                    self.timer.timeout.connect(self.data_send_select)
                self.timer.start(self.interval)
            except Exception as ret:
                self.messagebox_info('Bitte geben Sie ein zulässiges Zeitintervall ein/ms')
                self.Sendloop.setChecked(0)
        else:
            self.timer.stop()

    def click_select_open(self):
        '''
        启动按钮功能选择
        :return:
        '''
        self.prot_box.setEnabled(0)
        if self.prot_box.currentIndex() == 0:
            # 创建TCPServer
            self.socket_open_tcps()
            self.clients_list.addItem('All Connections')
        if self.prot_box.currentIndex() == 1:
            # 创建TCPClient
            self.socket_open_tcpc()
        if self.prot_box.currentIndex() == 2:
            # 创建UDPClient socket
            self.socket_open_udp()
        if self.working is True:
            self.statusbar_dict['status'].setText('Status：anschalten')

    def click_select_close(self):
        '''
        断开按钮功能选择
        :return:
        '''
        if self.Sendloop.isChecked():
            self.timer.stop()
        if self.prot_box.currentIndex() == 0:
            # 关闭TCPServer
            self.socket_close()
        if self.prot_box.currentIndex() == 1:
            # 断开TCPClient
            self.socket_close()
        if self.prot_box.currentIndex() == 2:
            # 关闭UDP socket
            self.socket_close_u()
        self.prot_box.setEnabled(1)
        self.statusbar_dict['status'].setText('Status：Schliessen')

    def data_send_select(self):
        ''' 发送按钮功能选择
        :return:
        '''
        if self.prot_box.currentIndex() == 0:
            self.data_send_t()
        if self.prot_box.currentIndex() == 1:
            self.data_send_t_c()
        if self.prot_box.currentIndex() == 2:
            self.data_send_u()

    def file_send_select(self):
        '''
        文件发送功能
        :return:
        '''
        if self.prot_box.currentIndex() == 0:
            self.file_send_t()
        if self.prot_box.currentIndex() == 1:
            self.file_send_t_c()
        if self.prot_box.currentIndex() == 2:
            self.file_send_u()

    def proto_imf(self):
        # 协议类型选择
        imf_s = self.prot_box.currentIndex()
        if imf_s == 0:
            self.clients_list.clear()
            self.localip_lb.setText('2.Local ip Addresse')
            self.localport_lb.setText('3.Local Portnummer')
            self.open_btn.setText('Beginne zuzuhören')
            self.clients_lbl.setText('Klient:')
            # 在tcp下不显示udp下的Remoteip，Remote端口标签
            self.clients_list.show()
            self.clients_lbl.show()
            self.remoteip_lbl.hide()
            self.remoteip_text.hide()
            self.remoteport_text.hide()
            self.remoteport_lbl.hide()
        if imf_s == 1:
            self.localip_lb.setText('2.Remote ip Addresse')
            self.localport_lb.setText('3.Remote Portnummer')
            self.open_btn.setText('verbinden')
            self.clients_lbl.setText('Remote Host:')
            self.clients_list.clear()
        if imf_s == 2:
            self.localip_lb.setText('2.LocalipAddresse')
            self.localport_lb.setText('3.LocalPortnummer')
            self.open_btn.setText('Beginne zuzuhören')
            self.clients_lbl.setText('Klient:')
            self.remoteip_lbl.show()
            self.remoteip_text.show()
            self.remoteport_text.show()
            self.remoteport_lbl.show()
            self.clients_list.hide()
            self.clients_lbl.hide()

    def recv_dataclear(self):
        """
        pushbutton_clear控件点击触发的槽
        :return: None
        """
        # 清空接收区屏幕
        self.DataRecvtext.clear()

    def send_dataclear(self):
        # 清空发送区框内容
        self.DataSendtext.clear()

    def rfilechoose(self):
        '''
        选择要保存的文件名
        :return:
        '''
        if self.recv2file.isChecked():
            '''接收转向文件'''
            file_name, ok = QFileDialog.getSaveFileName(
                self, u'save file', './', u'all file(*.*)')
            print(file_name)
            if ok:
                self.save_file_name = file_name
            else:
                self.save_file_name = None
    def send_fileload(self):
        '''
        hex to dec
        '''

            #
            # path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Text documents (*.txt);All files (*.*)")
            #
            # if path:
            #     try:
            #         with open(path, 'rt') as f:
            #             text = f.read()
            #
            #     except Exception as e:
            #         self.dialog_critical(str(e))
            #
            #     else:
            #         self.path = path
            #         self.editor.setPlainText(text)
            #         self.update_title()



    def datasave2file(self):
        '''
        将接收框中的消息保存到文件
        :return:
        '''
        if not self.DataRecvtext.toPlainText():
            QMessageBox.critical(self, 'Achtung', 'Derzeit werden keine Daten benötigt')
        else:
            file_name, state = QFileDialog.getSaveFileName(self, 'save file', './',
                                                           'Textfile(*.txt)')
            if state:
                with open(file_name, 'w', encoding='utf-8') as f_obj:
                    f_obj.write(self.DataRecvtext.toPlainText())
                QMessageBox.information(self, 'Erfolg', '%s Savefile Erfolg! ' % file_name)


                path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Text documents (*.txt);All files (*.*)")

                if path:
                    try:
                        with open(path, 'rt') as f:
                            text = f.read()

                    except Exception as e:
                        self.dialog_critical(str(e))

                    else:
                        self.path = path
                        self.editor.setPlainText(text)
                        self.update_title()







            # if state:
            #     with open(file_name, 'a', encoding='utf-8') as f_obj:
            #         f_obj.write(self.DataRecvtext.toPlainText())
            #     QMessageBox.information(self, 'Erfolg', '%s Savefile Erfolg! ' % file_name)

    def closeEvent(self, event):
        """
        对MainWindow的函数closeEvent进行重构
        退出软件时结束所有进程
        :param event:
        :return:
        """
        reply = QtWidgets.QMessageBox.question(self,
                                               'NetAssist',
                                               "Möchten Sie das Programm beenden?",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
            os._exit(0)
        else:
            event.ignore()

    # def show_ialweb(self):
    #     # import os
    #     os._exit(0)
    #     # print(p)
    #     # os.system('dir')


# class Child(QMainWindow,Ui_Child):
#   def __init__(self):
#     super(Child, self).__init__()
#     self.setupUi(self)
#     self.pushButton.clicked.connect(self.close)
#   def OPEN(self):
#     self.show()

    # if __name__ == "__main__":
    #     app = QApplication(sys.argv)
    #     main = Main()
    #     ch = Child()
    #     main.show()
    #     main.pushButton.clicked.connect(ch.OPEN)
    #     sys.exit(app.exec_())
if __name__ == "__main__":
    # app = QApplication(sys.argv)
    # myWin = PyQt5_Netassist()
    # 添加界面美化QCandyUI
    # myWin = CandyWindow.createWindow(myWin, 'blueGreen')
    # 如下是把翻译文件切换为中文
    # translator = QtCore.QTranslator()
    # translator.load("widgets_zh_CN.qm")
    # app.installTranslator(translator)
    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    loader = QUiLoader()

    app = QtWidgets.QApplication(sys.argv)
    window = loader.load("netAssitui.ui", None)
    # window.show()
    # app.exec_()
    # app = QApplication(sys.argv)
    # main = Ui_NetAssist()
    ch = Child()
    window.show()
    window.plotButton.clicked.connect(ch.OPEN)
    window.send_Btn.clicked.connect(PyQt5_Netassist.)


    # myWin.show()
    sys.exit(app.exec_())
