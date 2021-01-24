# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'netAssitui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_NetAssist(object):
    def setupUi(self, NetAssist):
        NetAssist.setObjectName("IAL_net")
        NetAssist.resize(821, 702)
        NetAssist.setStyleSheet(
            # "$text = #220200;"
            #                      "$background = #FFFFFF;"
            #                      "$border = #999999;"
            #                      "$selected = #8BF; "
            #                      "$pressed = #59F;"
            #                      "$focused = #EA2; "
            #                      "$grad1a = #EEEEEF;"
            #                      "$grad1b = #DADADF; "
            "QMainWindow {"
            "    background-color:#ececec;"

            "}"
            "QPushButton, QCommandLinkButton{"
            "     border: 2px solid transparent;"
            "    border-radius: 6px;"
            "    background-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 #84afe5, stop:1 #1168e4);\n"
            "     color: #FFFFFF;"
            "    min-width: 50px;"
            "    min-height: 16px;"
            "     }"
            "QPushButton::default, QToolButton::default, QCommandLinkButton::default{"
            "    border: 2px solid transparent;"
            "    color: #FFFFFF;"
            "    background-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 #84afe5, stop:1 #1168e4);\n"
            "}"
            "QPushButton:hover, QToolButton:hover, QCommandLinkButton:hover{"
            "    color: #220200;"
            "}"
            "QPushButton:pressed, QToolButton:pressed, QCommandLinkButton:pressed{"
            "    color: #aeaeae;"
            "    background-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 #ffffff, stop:0.5 #fbfdfd, stop:1 #ffffff); "
            "}"
            "QPushButton:disabled, QToolButton:disabled, QCommandLinkButton:disabled{"
            "    color: #616161;"
            "    background-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 #dce7eb, stop:0.5 #e0e8eb, stop:1 #dee7ec); "
            "} "
            )


    def retranslateUi(self, NetAssist):
        _translate = QtCore.QCoreApplication.translate
        NetAssist.setWindowTitle(_translate("NetAssist", "IAL_GaN_Messung"))
        self.RecvSettings.setTitle(_translate("NetAssist", "Empfangsbereichseinstellungen"))
        self.recv2file.setText(_translate("NetAssist", "Daten in Datei speichern"))
        self.newline.setText(_translate("NetAssist", "Anzeige automatisch umbrechen"))
        self.timestamp.setText(_translate("NetAssist", "Empfangszeit anzeigen"))
        self.stopdsp.setText(_translate("NetAssist", "Anzeige anhalten"))
        self.save_btn.setText(_translate("NetAssist", "Daten speichern"))
        self.hex_recv.setText(_translate("NetAssist", "Hexadezimale Anzeige"))
        self.clr_btn.setText(_translate("NetAssist", "Anzeige löschen"))
        self.NetSettings.setTitle(_translate("NetAssist", "Netzwerkeinstellungen"))
        self.prot_lb.setText(_translate("NetAssist", "1.ProtokollType"))
        self.prot_box.setItemText(0, _translate("NetAssist", "TCP Server"))
        self.prot_box.setItemText(1, _translate("NetAssist", "TCP Client"))
        self.prot_box.setItemText(2, _translate("NetAssist", "UDP"))
        self.localip_lb.setText(_translate("NetAssist", "2.Lokale IP-Adresse"))
        self.Localip_lineedit.setText(_translate("NetAssist", "192.168.1.88"))
        self.localport_lb.setText(_translate("NetAssist", "3.Lokale Portnummer"))
        self.Localport_lineedit.setText(_translate("NetAssist", "5000"))
        self.open_btn.setText(_translate("NetAssist", "Beginne zuzuhören"))
        self.close_btn.setText(_translate("NetAssist", "trennen"))
        self.SendSettings.setTitle(_translate("NetAssist", "Einstellungen senden"))
        self.Sendloop.setText(_translate("NetAssist", "Periodische Übertragung"))
        self.ms_lbl.setText(_translate("NetAssist", "ms"))
        self.Sendclear.setText(_translate("NetAssist", "Nach dem Senden automatisch löschen"))
        self.Sendcheck.setText(_translate("NetAssist", "Zusätzliche Bits automatisch senden"))
        self.file_send_btn.setText(_translate("NetAssist", "Dateien senden"))
        self.hex_send.setText(_translate("NetAssist", "Hexadezimales Senden"))
        self.clr_btn2.setText(_translate("NetAssist", "Anzeige löschen"))
        self.file_load.setText(_translate("NetAssist", "Lade Datei"))
        self.Datarecv.setTitle(_translate("NetAssist", "Netzwerkdatenempfang"))
        self.clients_lbl.setText(_translate("NetAssist", "Klient:"))
        self.remoteip_lbl.setText(_translate("NetAssist", "Remote-IP"))
        self.remoteport_lbl.setText(_translate("NetAssist", "Die Portnummer"))
        self.Datasend.setTitle(_translate("NetAssist", "Daten senden"))
        self.send_Btn.setText(_translate("NetAssist", "senden"))

