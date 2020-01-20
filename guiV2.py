# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindowV2.ui'
##
## Created by: Qt User Interface Compiler version 5.14.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1342, 667)
        self.centralWidget = QWidget(MainWindow)
        self.centralWidget.setObjectName(u"centralWidget")
        self.carpetaChooser = QPushButton(self.centralWidget)
        self.carpetaChooser.setObjectName(u"carpetaChooser")
        self.carpetaChooser.setGeometry(QRect(50, 440, 171, 31))
        self.impresora = QPushButton(self.centralWidget)
        self.impresora.setObjectName(u"impresora")
        self.impresora.setGeometry(QRect(730, 580, 211, 31))
        self.imprimir = QPushButton(self.centralWidget)
        self.imprimir.setObjectName(u"imprimir")
        self.imprimir.setEnabled(False)
        self.imprimir.setGeometry(QRect(730, 540, 211, 31))
        self.listaDeImpresoras = QListWidget(self.centralWidget)
        self.listaDeImpresoras.setObjectName(u"listaDeImpresoras")
        self.listaDeImpresoras.setEnabled(False)
        self.listaDeImpresoras.setGeometry(QRect(960, 540, 371, 71))
        self.folder = QLabel(self.centralWidget)
        self.folder.setObjectName(u"folder")
        self.folder.setGeometry(QRect(260, 540, 441, 51))
        self.folderPDF = QLabel(self.centralWidget)
        self.folderPDF.setObjectName(u"folderPDF")
        self.folderPDF.setGeometry(QRect(260, 590, 441, 21))
        self.tableWidget_xml = QTableWidget(self.centralWidget)
        self.tableWidget_xml.setObjectName(u"tableWidget_xml")
        self.tableWidget_xml.setGeometry(QRect(0, 10, 1341, 415))
        self.tableWidget_xml.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.tableWidget_xml.setSortingEnabled(True)
        self.tableWidget_resumen = QTableWidget(self.centralWidget)
        self.tableWidget_resumen.setObjectName(u"tableWidget_resumen")
        self.tableWidget_resumen.setGeometry(QRect(251, 440, 911, 62))
        self.tableWidget_resumen.setAutoScroll(True)
        self.tableWidget_resumen.horizontalHeader().setVisible(False)
        self.tableWidget_resumen.horizontalHeader().setMinimumSectionSize(50)
        self.tableWidget_resumen.horizontalHeader().setHighlightSections(False)
        self.tableWidget_resumen.verticalHeader().setVisible(False)
        self.labelLogo = QLabel(self.centralWidget)
        self.labelLogo.setObjectName(u"labelLogo")
        self.labelLogo.setGeometry(QRect(80, 520, 131, 91))
        self.descarga_bt = QPushButton(self.centralWidget)
        self.descarga_bt.setObjectName(u"descarga_bt")
        self.descarga_bt.setGeometry(QRect(50, 470, 171, 23))
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 1342, 21))
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QToolBar(MainWindow)
        self.mainToolBar.setObjectName(u"mainToolBar")
        MainWindow.addToolBar(Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QStatusBar(MainWindow)
        self.statusBar.setObjectName(u"statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Huiini 1.0", None))
        self.carpetaChooser.setText(QCoreApplication.translate("MainWindow", u"Selecciona Carpeta", None))
        self.impresora.setText(QCoreApplication.translate("MainWindow", u"Selecciona Impresora", None))
        self.imprimir.setText(QCoreApplication.translate("MainWindow", u"Imprimir", None))
        self.folder.setText("")
        self.folderPDF.setText("")
        self.labelLogo.setText("")
        self.descarga_bt.setText(QCoreApplication.translate("MainWindow", u"Descarga SAT", None))
    # retranslateUi

