#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    :  
# @Author  :  
# @Site    :
# @File    : tcp_udp_ui.py
# @Software: PyCharm
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal
from netAssitui import Ui_NetAssist
from time import ctime
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QDialog
import binascii


class Tcp_ucpUi(Ui_NetAssist):
    # 主线程属性继承自Ui_NetAssist
    # 信号槽机制：设置一个信号，用于触发接收区写入动作
    signal_write_msg = pyqtSignal(str)
    signal_status_connected = pyqtSignal(str)
    signal_status_removed = pyqtSignal(str)
    signal_add_clientstatus_info = pyqtSignal(str)
    signal_messagebox_info = pyqtSignal(str)

    # statusbar上添加的控件
    # 使用字典方式进行管理
    statusbar_dict = {}
    rx_count = 0
    tx_count = 0
    # statusbar End
    tail_ok = False

    def __init__(self):
        super(Tcp_ucpUi, self).__init__()

    def custom_connect(self):
        """
        控件信号-槽的设置
        :param : QDialog类创建的对象
        :return: None
        """
        self.signal_write_msg.connect(self.write_msg)
        self.signal_status_connected.connect(self.statusbar_connect)
        self.signal_status_removed.connect(self.statusbar_remove)
        self.signal_add_clientstatus_info.connect(self.add_clientstatus_plain)
        self.signal_messagebox_info.connect(self.messagebox_info)

    def send_fileload(self):
        """
        载入文件功能
        :return:
        """
        if self.file_load.isChecked():
            # 载入发送文件
            send_file_name, sf_ok = QFileDialog.getOpenFileName(
                self, u'Dokument speichern', './', u'Alle Dateien(*.*)')
            if sf_ok:
                self.statusbar.showMessage('Datei erfolgreich geladen', msecs=3000)
                with open(send_file_name, 'rb') as send_f:
                    self.f_data = send_f.read()
                print(self.f_data)
            else:
                self.file_load.setChecked(False)
                self.statusbar.showMessage('Das Laden der Datei ist fehlgeschlagen', msecs=3000)

    def add_clientstatus_plain(self, info):
        # signal_add_clientstatus_info信号会触发本函数
        """
        向接收框发送客户端连接信息
        :param info:
        :return:
        """
        self.DataRecvtext.insertPlainText(info)

    def messagebox_info(self, info):
        # signal_messagebox_info信号会触发本函数
        """
        弹出消息框
        :param info:
        :return:
        """
        QMessageBox.critical(self, 'Error', info)

    def write_msg(self, msg):
        # signal_write_msg信号会触发这个函数
        """
        功能函数，向接收区写入数据的方法
        信号-槽触发
        tip：PyQt程序的子线程中，直接向主线程的界面传输字符是不符合安全原则的
        :return: None
        """
        # 为接收到的数据加上时间戳并且显示在接收框中
        if self.timestamp.isChecked():
            if self.newline.isChecked():
                self.DataRecvtext.insertPlainText('[%s]\n' % ctime())
                self.DataRecvtext.insertPlainText('%s' % msg)
            else:
                self.DataRecvtext.insertPlainText('[%s]' % ctime())
                self.DataRecvtext.insertPlainText('%s' % msg)
        else:
            if self.newline.isChecked():
                self.DataRecvtext.insertPlainText('%s\n' % msg)
            else:
                self.DataRecvtext.insertPlainText('%s' % msg)
        # 滚动条移动到结尾
        self.DataRecvtext.moveCursor(QtGui.QTextCursor.End)

    def comboBox_removeItem_byName(self, combo, name):
        '''QComboBox中删除特定名字的项目'''
        for i in range(0, combo.count()):
            if name == combo.itemText(i):
                # 找到对应的项目
                combo.removeItem(i)

    def statusbar_connect(self, statusbar_client_info):
        # signal_messagebox_info信号会触发本函数
        self.statusbar.showMessage(
            'Klient:%s Erfolgreich verbunden!' %
            statusbar_client_info, msecs=2000)

    def statusbar_remove(self, statusbar_client_info):
        # signal_status_removed信号会触发本函数
        self.statusbar.showMessage(
            'Klient:%s Trennen!' %
            statusbar_client_info, msecs=2000)

    def str_to_hex(self, s):
        """
        字符串转16进制显示
        :param s:
        :return:
        """
        return ' '.join([hex(ord(c)).replace('0x', '') for c in s])

    def hex_to_str(self, s):
        """
        16进制转字符串显示
        :param s:
        :return:
        """
        return ''.join([chr(i) for i in [int(b, 16) for b in s.split(' ')]])

    def str_to_bin(self, s):
        """
        字符串转二进制显示
        :param s:
        :return:
        """
        return ' '.join([bin(ord(c)).replace('0b', '') for c in s])

    def bin_to_str(self, s):
        """
        二进制转字符串显示
        :param s:
        :return:
        """
        return ''.join([chr(i) for i in [int(b, 2) for b in s.split(' ')]])

    def hex_show(self, str):
        """
        将字符串转换为大写字母并每隔2个字符用空格分割处理后得到一个新字符串
        如：faa5fbb5fcc5fdd5010200000028000001900000000a002d00000000017d7840000003e800005fa55fb55fc55fd5
            FA A5 FB B5 FC C5 FD D5 01 02 00 00 00 28 00 00 01 90 00 00 00 0A 00 2D 00 00 00 00 01 7D 78 40 00 00 03 E8 00 00 5F A5 5F B5 5F C5 5F D5
        :param str:
        :return:
        """
        t = str.upper()
        return ' '.join([t[2 * i:2 * (i + 1)] for i in range(len(t) // 2)])
        # / 是精确除法， // 是向下取整除法， % 是求模

    def if_hex_send(self, pre_msg):
        """
        判断是否以16进制发送并处理
        :param pre_msg:
        :return:
        """
        try:
            if self.hex_send.isChecked():
                send_msg = pre_msg.replace(' ', '')  # 删除无效的空格
                if len(send_msg) % 2 != 0:
                    # 十六进制发送输入的长度必须是2的倍数
                    raise Exception('Die Länge der hexadezimalen Eingabe muss ein Vielfaches von 2 sein')
                send_msg = binascii.a2b_hex(send_msg)
            else:
                send_msg = pre_msg.encode('utf-8')
            return send_msg

        except binascii.Error as e:
            QMessageBox.critical(self, 'Error', 'Die Hexadezimalzahl enthält unzulässige Zeichen!')
        except Exception as e:
            QMessageBox.critical(self, 'Error', '%s' % e)

    def if_hex_show_tcpc_udp(self, pre_msg):
        """
        判断是否以16进制显示并处理
        :param pre_msg:
        :return:
        """
        if self.hex_recv.isChecked():
            msg = binascii.b2a_hex(pre_msg).decode('utf-8')
            print(msg, type(msg), len(msg))  # msg为 str 类型
            msg = self.hex_show(msg)  # 将解码后的16进制数据按照两个字符+'空字符'发送到接收框中显示
            self.signal_write_msg.emit(msg)
        else:
            try:
                # 尝试对接收到的数据解码，如果解码成功，即使解码后的数据是ascii可显示字符也直接发送，
                msg = pre_msg.decode('utf-8')
                print(msg)
                self.signal_write_msg.emit(msg)
            except Exception as ret:
                # 如果出现解码错误，提示用户选中16进制显示
                self.signal_messagebox_info.emit('Dekodierungsfehler, bitte versuchen Sie es mit einer hexadezimalen Anzeige')

    def checksend_choose(self):
        '''
        勾选添加附加位toggle之后的动作
        :return:
        '''
        if self.Sendcheck.isChecked():
            self.checkDialog = QDialog()
            self.checkDialog.resize(381, 200)
            self.checkDialog.setMinimumSize(QtCore.QSize(381, 200))
            self.checkDialog.setMaximumSize(QtCore.QSize(381, 200))
            self.checkDialog.setWindowTitle('Zusätzliche Biteinstellung')
            self.widget = QtWidgets.QWidget(self.checkDialog)
            self.widget.setGeometry(QtCore.QRect(90, 160, 195, 30))
            self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
            self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
            self.okBtn = QtWidgets.QPushButton(self.widget)
            self.okBtn.setText('bestimmen')
            self.horizontalLayout.addWidget(self.okBtn)
            self.cancelBtn = QtWidgets.QPushButton(self.widget)
            self.cancelBtn.setText('stornieren')
            self.horizontalLayout.addWidget(self.cancelBtn)
            self.groupBox = QtWidgets.QGroupBox(self.checkDialog)
            self.groupBox.setGeometry(QtCore.QRect(10, 10, 361, 141))
            self.rBtn1 = QtWidgets.QRadioButton(self.groupBox)
            self.rBtn1.setGeometry(QtCore.QRect(12, 27, 72, 19))
            self.rBtn2 = QtWidgets.QRadioButton(self.groupBox)
            self.rBtn2.setGeometry(QtCore.QRect(12, 53, 72, 19))
            self.rBtn3 = QtWidgets.QRadioButton(self.groupBox)
            self.rBtn3.setGeometry(QtCore.QRect(12, 80, 151, 19))
            self.lineEdit = QtWidgets.QLineEdit(self.groupBox)
            self.lineEdit.setGeometry(QtCore.QRect(170, 80, 41, 21))
            self.lineEdit.setText('0d')
            self.groupBox.setTitle("Zusätzliche Biteinstellung")
            self.rBtn1.setText("Methode eins")
            self.rBtn2.setText("Methode Zwei")
            self.rBtn3.setText("Fixierte Position (Hexadezimal)")
            self.okBtn.clicked.connect(self.ok)
            self.cancelBtn.clicked.connect(self.cancel)
            self.rBtn1.toggled.connect(self.settail_1)
            self.rBtn2.toggled.connect(self.settail_2)
            self.rBtn3.toggled.connect(self.settail_3)
            self.checkDialog.exec_()

    def ok(self):
        '''
        “确认”按钮按下后的动作
        :return:
        '''
        if self.rBtn1.isChecked() or self.rBtn2.isChecked() or self.rBtn3.isChecked():
            print('bestimmen')
            self.checkDialog.close()
        else:
            print('Ich habe keine Methode gewählt')
            self.Sendcheck.setChecked(0)
            self.checkDialog.close()

    def cancel(self):
        '''
        “取消”按钮按下后的动作
        :return:
        '''
        print('取消')
        self.Sendcheck.setChecked(0)
        self.checkDialog.close()

    def settail_1(self):
        '''
        勾选方法一
        :return:
        '''
        if self.rBtn1.isChecked():
            # 添加附加位标志位的RadioButton勾选状态为Tue
            self.tail_ok = True
            # 添加附加位，当前设置为'f1'
            self.append_tail = 'f1'
            print('rBtn1 checked')
            print(self.tail_ok)

    def settail_2(self):
        '''
        勾选方法二
        :return:
        '''
        if self.rBtn2.isChecked():
            # 添加附加位标志位的RadioButton勾选状态为Tue
            self.tail_ok = True
            # 添加附加位，当前设置为'f2'
            self.append_tail = 'f2'
            print('rBtn2 checked')
            print(self.tail_ok)

    def settail_3(self):
        '''
        勾选方法三（固定位）
        :return:
        '''
        if self.rBtn3.isChecked():
            # 添加附加位标志位的RadioButton勾选状态为Tue
            self.tail_ok = True
            # 添加附加位，由用户自行添加
            self.append_tail = self.lineEdit.text()
            print('rBtn3 checked')
            print(self.tail_ok)

    def is_sendcheck_send(self, get_msg):
        '''
        判断是否进行附加位发送
        :param get_msg:
        :return:
        '''
        # 判断自动发送附加位combobox是否按下
        if self.Sendcheck.isChecked():
            # 判断附加位设置Dialog中的RadioButton是否选中
            if self.tail_ok:
                get_msg_c = get_msg + self.append_tail
                print(get_msg_c)
                # 返回加入附加位的新内容
                return get_msg_c
            else:
                # 如果RadioButton未选中，返回初始消息
                return get_msg
        else:
            # 如果自动发送附加位combobox未按下，返回初始消息
            return get_msg
