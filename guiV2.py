# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindowV2.ui',
# licensing of 'mainwindowV2.ui' applies.
#
# Created: Thu Dec 17 21:53:30 2020
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1342, 667)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.carpetaChooser = QtWidgets.QPushButton(self.centralWidget)
        self.carpetaChooser.setGeometry(QtCore.QRect(50, 440, 171, 31))
        self.carpetaChooser.setObjectName("carpetaChooser")
        self.impresora = QtWidgets.QPushButton(self.centralWidget)
        self.impresora.setGeometry(QtCore.QRect(820, 580, 121, 31))
        self.impresora.setObjectName("impresora")
        self.imprimir = QtWidgets.QPushButton(self.centralWidget)
        self.imprimir.setEnabled(False)
        self.imprimir.setGeometry(QtCore.QRect(700, 540, 241, 31))
        self.imprimir.setObjectName("imprimir")
        self.listaDeImpresoras = QtWidgets.QListWidget(self.centralWidget)
        self.listaDeImpresoras.setEnabled(False)
        self.listaDeImpresoras.setGeometry(QtCore.QRect(960, 540, 371, 71))
        self.listaDeImpresoras.setObjectName("listaDeImpresoras")
        self.folder = QtWidgets.QLabel(self.centralWidget)
        self.folder.setGeometry(QtCore.QRect(260, 540, 411, 51))
        self.folder.setText("")
        self.folder.setObjectName("folder")
        self.folderPDF = QtWidgets.QLabel(self.centralWidget)
        self.folderPDF.setGeometry(QtCore.QRect(260, 590, 441, 21))
        self.folderPDF.setText("")
        self.folderPDF.setObjectName("folderPDF")
        self.tableWidget_xml = QtWidgets.QTableWidget(self.centralWidget)
        self.tableWidget_xml.setGeometry(QtCore.QRect(0, 10, 1341, 415))
        self.tableWidget_xml.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.tableWidget_xml.setObjectName("tableWidget_xml")
        self.tableWidget_xml.setColumnCount(0)
        self.tableWidget_xml.setRowCount(0)
        self.tableWidget_resumen = QtWidgets.QTableWidget(self.centralWidget)
        self.tableWidget_resumen.setGeometry(QtCore.QRect(251, 440, 911, 62))
        self.tableWidget_resumen.setAutoScroll(True)
        self.tableWidget_resumen.setObjectName("tableWidget_resumen")
        self.tableWidget_resumen.setColumnCount(0)
        self.tableWidget_resumen.setRowCount(0)
        self.tableWidget_resumen.horizontalHeader().setVisible(False)
        self.tableWidget_resumen.horizontalHeader().setHighlightSections(False)
        self.tableWidget_resumen.horizontalHeader().setMinimumSectionSize(50)
        self.tableWidget_resumen.verticalHeader().setVisible(False)
        self.labelLogo = QtWidgets.QLabel(self.centralWidget)
        self.labelLogo.setGeometry(QtCore.QRect(80, 520, 131, 91))
        self.labelLogo.setText("")
        self.labelLogo.setObjectName("labelLogo")
        self.agrega_cats = QtWidgets.QPushButton(self.centralWidget)
        self.agrega_cats.setEnabled(False)
        self.agrega_cats.setGeometry(QtCore.QRect(50, 470, 171, 31))
        self.agrega_cats.setObjectName("agrega_cats")
        self.botonCancela = QtWidgets.QPushButton(self.centralWidget)
        self.botonCancela.setGeometry(QtCore.QRect(700, 580, 111, 31))
        self.botonCancela.setObjectName("botonCancela")
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1342, 21))
        self.menuBar.setObjectName("menuBar")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "Huiini 1.0", None, -1))
        self.carpetaChooser.setText(QtWidgets.QApplication.translate("MainWindow", "Selecciona Carpeta", None, -1))
        self.impresora.setText(QtWidgets.QApplication.translate("MainWindow", "Selecciona Impresora", None, -1))
        self.imprimir.setText(QtWidgets.QApplication.translate("MainWindow", "Imprimir", None, -1))
        self.tableWidget_xml.setSortingEnabled(True)
        self.agrega_cats.setText(QtWidgets.QApplication.translate("MainWindow", "Agrega categorías", None, -1))
        self.botonCancela.setText(QtWidgets.QApplication.translate("MainWindow", "Cancelar impresión", None, -1))

