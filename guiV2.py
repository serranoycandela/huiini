# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindowV2.ui'
#
# Created: Sat Oct 06 14:09:49 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1342, 667)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.carpetaChooser = QtGui.QPushButton(self.centralWidget)
        self.carpetaChooser.setGeometry(QtCore.QRect(50, 440, 171, 31))
        self.carpetaChooser.setObjectName("carpetaChooser")
        self.impresora = QtGui.QPushButton(self.centralWidget)
        self.impresora.setGeometry(QtCore.QRect(730, 580, 211, 31))
        self.impresora.setObjectName("impresora")
        self.imprimir = QtGui.QPushButton(self.centralWidget)
        self.imprimir.setEnabled(False)
        self.imprimir.setGeometry(QtCore.QRect(730, 540, 211, 31))
        self.imprimir.setObjectName("imprimir")
        self.listaDeImpresoras = QtGui.QListWidget(self.centralWidget)
        self.listaDeImpresoras.setEnabled(False)
        self.listaDeImpresoras.setGeometry(QtCore.QRect(960, 540, 371, 71))
        self.listaDeImpresoras.setObjectName("listaDeImpresoras")
        self.folder = QtGui.QLabel(self.centralWidget)
        self.folder.setGeometry(QtCore.QRect(260, 540, 441, 51))
        self.folder.setText("")
        self.folder.setObjectName("folder")
        self.folderPDF = QtGui.QLabel(self.centralWidget)
        self.folderPDF.setGeometry(QtCore.QRect(260, 590, 441, 21))
        self.folderPDF.setText("")
        self.folderPDF.setObjectName("folderPDF")
        self.tableWidget_xml = QtGui.QTableWidget(self.centralWidget)
        self.tableWidget_xml.setGeometry(QtCore.QRect(0, 10, 1341, 415))
        self.tableWidget_xml.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.tableWidget_xml.setObjectName("tableWidget_xml")
        self.tableWidget_xml.setColumnCount(0)
        self.tableWidget_xml.setRowCount(0)
        self.tableWidget_resumen = QtGui.QTableWidget(self.centralWidget)
        self.tableWidget_resumen.setGeometry(QtCore.QRect(251, 440, 911, 62))
        self.tableWidget_resumen.setAutoScroll(True)
        self.tableWidget_resumen.setObjectName("tableWidget_resumen")
        self.tableWidget_resumen.setColumnCount(0)
        self.tableWidget_resumen.setRowCount(0)
        self.tableWidget_resumen.horizontalHeader().setVisible(False)
        self.tableWidget_resumen.horizontalHeader().setHighlightSections(False)
        self.tableWidget_resumen.horizontalHeader().setMinimumSectionSize(50)
        self.tableWidget_resumen.verticalHeader().setVisible(False)
        self.labelLogo = QtGui.QLabel(self.centralWidget)
        self.labelLogo.setGeometry(QtCore.QRect(80, 520, 131, 91))
        self.labelLogo.setText("")
        self.labelLogo.setObjectName("labelLogo")
        self.descarga_bt = QtGui.QPushButton(self.centralWidget)
        self.descarga_bt.setGeometry(QtCore.QRect(50, 470, 171, 23))
        self.descarga_bt.setObjectName("descarga_bt")
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1342, 21))
        self.menuBar.setObjectName("menuBar")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtGui.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Huiini 1.0", None, QtGui.QApplication.UnicodeUTF8))
        self.carpetaChooser.setText(QtGui.QApplication.translate("MainWindow", "Selecciona Carpeta", None, QtGui.QApplication.UnicodeUTF8))
        self.impresora.setText(QtGui.QApplication.translate("MainWindow", "Selecciona Impresora", None, QtGui.QApplication.UnicodeUTF8))
        self.imprimir.setText(QtGui.QApplication.translate("MainWindow", "Imprimir", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget_xml.setSortingEnabled(True)
        self.descarga_bt.setText(QtGui.QApplication.translate("MainWindow", "Descarga SAT", None, QtGui.QApplication.UnicodeUTF8))

