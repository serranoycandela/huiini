#-*- encoding: utf-8 -*-
from PySide.QtCore import *
import requests
from PySide.QtCore import Qt
from PySide.QtGui import *
from PySide import QtGui
import sys
import guiV2
from os import listdir
from os.path import isfile, join, basename
import shutil
import os

import time as time_old
from subprocess import Popen
#import jinja2
from FacturasClient import FacturaClient as Factura
import math
import json

## para instalar pyside en macos 10.13
## brew tap cartr/qt4
## brew tap-pin cartr/qt4
## brew install qt@4
## virtualenv --python /Library/Frameworks/Python.framework/Versions/3.4/bin/python3.4 venv
## source venv/bin/activate
## python setup.py bdist_wheel --ignore-git --qmake=/usr/local/Cellar/qt@4/4.8.7_3/bin/qmake --cmake=/Applications/CMake.app/Contents/bin/cmake
## pip install PySide-1.2.4-cp34-cp34m-macosx_10_6_intel.whl

## ademas ocupa urllib3 y requests
## pip install urllib3
## pip install requests


##pyside-uic mainwindow.ui -o gui.py
##pyside-uic mainwindowV2.ui -o guiV2.py
class ImgWidget1(QtGui.QLabel):

    def __init__(self, parent=None):
        super(ImgWidget1, self).__init__(parent)
        pic = QtGui.QPixmap("palomita.png")
        self.setPixmap(pic)

class ImgWidget2(QtGui.QLabel):

    def __init__(self, parent=None):
        super(ImgWidget2, self).__init__(parent)
        pic = QtGui.QPixmap("x.png")
        self.setPixmap(pic)

class Ui_MainWindow(QMainWindow, guiV2.Ui_MainWindow):

    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__(parent)
        self.setupUi(self)

        logoPix = QtGui.QPixmap("logo.png")
        self.labelLogo.setPixmap(logoPix)
        self.pdflatex_path = "C:/Program Files/MiKTeX 2.9/miktex/bin/x64/pdflatex.exe"

        self.carpetaChooser.clicked.connect(self.cualCarpeta)
        self.imprimir.clicked.connect(self.imprime)

        self.impresora.clicked.connect(self.cambiaImpresora)
        self.listaDeImpresoras.currentItemChanged.connect(self.cambiaSeleccionDeImpresora)

        self.tableWidget_xml.setColumnCount(16)
        self.tableWidget_xml.setColumnWidth(0,30)#pdf
        self.tableWidget_xml.setColumnWidth(1,95)#fecha
        self.tableWidget_xml.setColumnWidth(2,70)#uuid
        self.tableWidget_xml.setColumnWidth(3,120)#receptor-nombre
        self.tableWidget_xml.setColumnWidth(4,120)#emisor-rfc
        self.tableWidget_xml.setColumnWidth(5,120)#concepto
        self.tableWidget_xml.setColumnWidth(6,30)#version
        self.tableWidget_xml.setColumnWidth(7,75)#Subtotal
        self.tableWidget_xml.setColumnWidth(8,80)#Descuento
        self.tableWidget_xml.setColumnWidth(9,80)#traslados-iva
        self.tableWidget_xml.setColumnWidth(10,80)#traslados-ieps
        self.tableWidget_xml.setColumnWidth(11,75)#retIVA
        self.tableWidget_xml.setColumnWidth(12,75)#retISR
        self.tableWidget_xml.setColumnWidth(13,80)#total
        self.tableWidget_xml.setColumnWidth(14,74)#formaDePago
        self.tableWidget_xml.setColumnWidth(15,77)#metodoDePago

        self.tableWidget_xml.verticalHeader().setFixedWidth(35)

        self.tableWidget_resumen.setColumnCount(10)
        self.tableWidget_resumen.setColumnWidth(0,30)
        self.tableWidget_resumen.setColumnWidth(1,152)
        self.tableWidget_resumen.setColumnWidth(2,192)
        self.tableWidget_resumen.setColumnWidth(3,80)
        self.tableWidget_resumen.setColumnWidth(4,80)
        self.tableWidget_resumen.setColumnWidth(5,80)
        self.tableWidget_resumen.setColumnWidth(6,80)
        self.tableWidget_resumen.setColumnWidth(7,65)
        self.tableWidget_resumen.setColumnWidth(8,65)
        self.tableWidget_resumen.setColumnWidth(9,80)
        self.tableWidget_resumen.setRowCount(2)
        #self.tableWidget_resumen.verticalHeader().setFixedWidth(35)

        header = self.tableWidget_xml.verticalHeader()
        header.setContextMenuPolicy(Qt.CustomContextMenu)
        header.customContextMenuRequested.connect(self.handleHeaderMenu)

        self.ponEncabezado()

        self.tableWidget_xml.cellDoubleClicked.connect(self.meDoblePicaronXML)
        self.tableWidget_resumen.cellDoubleClicked.connect(self.meDoblePicaronResumen)



    def hazResumenDiot(self,currentDir):
        sumaSubTotal = 0
        sumaDescuento = 0
        sumaTrasladoIVA = 0
        sumaImporte = 0
        sumaTotal = 0
        for key, value in self.diccionarioPorRFCs.items():
            sumaSubTotal += value['subTotal']
            sumaDescuento += value['descuento']
            sumaTrasladoIVA += value['trasladoIVA']
            sumaImporte += value['importe']
            sumaTotal += value['total']

        self.listaDiot = []

        contador = 0
        tablaIndex = 0
        listaAcotada = []
        for key, value in self.diccionarioPorRFCs.items():
            contador += 1
            if contador > 60:
                contador = 1
                tablaIndex +=1
                self.listaDiot.append(listaAcotada)
                listaAcotada = []


            listaAcotada.append({'rfc' : key,
                                   'subTotal': value['subTotal'],
                                   'descuento': value['descuento'],
                                   'trasladoIVA': value['trasladoIVA'],
                                   'importe': value['importe'],
                                   'total': value['total']
                                    })


        listaAcotada.append({'rfc' : 'Suma',
                               'subTotal': sumaSubTotal,
                               'descuento': sumaDescuento,
                               'trasladoIVA': sumaTrasladoIVA,
                               'importe': sumaImporte,
                                'total': sumaTotal
                                })

        self.listaDiot.append(listaAcotada)

        for key, value in self.diccionarioPorRFCs.items():
            print(key, value)

        url_get = "http://huiini.pythonanywhere.com/resumen"

        r = requests.get(url_get, params={'lista_diot': json.dumps(self.listaDiot)}, stream=True)
        time_old.sleep(1)
        if r.status_code == 200:
            with open(join(self.esteFolder, 'resumenDiot.pdf'),'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)



    def hazListadeUuids(self):
        self.listadeUuids = []
        for renglon in range(self.numeroDeFacturasValidas):
            self.listadeUuids.append(self.tableWidget_xml.item(renglon,1).text())


    def handleHeaderMenu(self, pos):
        menu = QtGui.QMenu()
        deleteAction = QtGui.QAction('&Delete', self)
        #deleteAction = QtGui.QAction("Delete")
        deleteAction.triggered.connect(lambda: self.quitaRenglon(self.tableWidget_xml.verticalHeader().logicalIndexAt(pos)))
        menu.addAction(deleteAction)

        menu.exec_(QtGui.QCursor.pos())

    def quitaRenglon(self,row):
        elNombre = self.tableWidget_xml.item(row,2).text()
        suRFC = ""
        for factura in self.listaDeFacturasOrdenadas:
            if factura.UUID == elNombre:
                print("i found it!")
                suRFC = factura.EmisorRFC

                break


        suSubtotal = float(self.tableWidget_xml.item(row,7).text())
        suDescuento = float(self.tableWidget_xml.item(row,8).text())
        suTrasladoIVA = float(self.tableWidget_xml.item(row,9).text())
        suImporte = float(self.tableWidget_xml.item(row,7).text())-float(self.tableWidget_xml.item(row,8).text())
        self.tableWidget_xml.removeRow(row)

        if suRFC in self.diccionarioPorRFCs:
            self.diccionarioPorRFCs[suRFC]['subTotal'] -= suSubtotal
            self.diccionarioPorRFCs[suRFC]['descuento'] -= suDescuento
            self.diccionarioPorRFCs[suRFC]['trasladoIVA'] -= suTrasladoIVA
            self.diccionarioPorRFCs[suRFC]['importe'] -= suImporte

            if math.fabs(self.diccionarioPorRFCs[suRFC]['subTotal']) < 0.0001 and math.fabs(self.diccionarioPorRFCs[suRFC]['descuento']) < 0.0001 and math.fabs(self.diccionarioPorRFCs[suRFC]['trasladoIVA']) < 0.0001 and math.fabs(self.diccionarioPorRFCs[suRFC]['importe']) < 0.0001:
                self.diccionarioPorRFCs.pop(suRFC,0)


        self.numeroDeFacturasValidas -= 1
        self.sumale(1)
        self.hazResumenDiot(self.esteFolder)
        try:
            if os.path.exists(os.path.join(os.path.join(self.esteFolder,"pdfs"),"resumenDiot.pdf")):

                os.remove(os.path.join(os.path.join(self.esteFolder,"pdfs"),"resumenDiot.pdf"))

            os.rename(os.path.join(self.esteFolder,"resumenDiot.pdf"), os.path.join(os.path.join(self.esteFolder,"pdfs"),"resumenDiot.pdf"))
        except:
            QtGui.QMessageBox.information(self, "Information", "tienes abierto el resumenDiot.pdf")


    def sumale(self, renglonResumen=0):
        for columna in range(7,14):
            suma = 0
            for renglon in range(self.numeroDeFacturasValidas):

                suma += float(self.tableWidget_xml.item(renglon, columna).text())


            self.tableWidget_resumen.setItem(renglonResumen,columna-4,QTableWidgetItem(str(suma)))

        if renglonResumen == 1:
            self.tableWidget_resumen.setItem(0,1,QTableWidgetItem("            ---------"))
            self.tableWidget_resumen.setItem(0,2,QTableWidgetItem("Sumatoria del Periodo Original"))
            self.tableWidget_resumen.setItem(1,1,QTableWidgetItem("Resumen Diot Actualizado"))
            self.tableWidget_resumen.setItem(1,2,QTableWidgetItem("Sumatoria del Periodo Actualizada"))
            self.tableWidget_resumen.setCellWidget(1,0,ImgWidget1(self))
            self.tableWidget_resumen.setCellWidget(0,0,ImgWidget2(self))


    def ponEncabezado(self):
        itemVersion = QTableWidgetItem("V")
        itemVersion.setToolTip("Versión")
        self.tableWidget_xml.setHorizontalHeaderItem (0, QTableWidgetItem("Pdf"))
        self.tableWidget_xml.setHorizontalHeaderItem (1, QTableWidgetItem("Fecha"))
        self.tableWidget_xml.setHorizontalHeaderItem (2, QTableWidgetItem("UUID"))
        self.tableWidget_xml.setHorizontalHeaderItem (3, QTableWidgetItem("Receptor"))
        self.tableWidget_xml.setHorizontalHeaderItem (4, QTableWidgetItem("Emisor"))
        self.tableWidget_xml.setHorizontalHeaderItem (5, QTableWidgetItem("Concepto"))
        self.tableWidget_xml.setHorizontalHeaderItem (6, itemVersion)
        self.tableWidget_xml.setHorizontalHeaderItem (7, QTableWidgetItem("Subtotal"))
        self.tableWidget_xml.setHorizontalHeaderItem (8, QTableWidgetItem("Descuento"))
        self.tableWidget_xml.setHorizontalHeaderItem (9, QTableWidgetItem("Traslado\nIVA"))
        self.tableWidget_xml.setHorizontalHeaderItem (10, QTableWidgetItem("Traslado\nIEPS"))
        self.tableWidget_xml.setHorizontalHeaderItem (11, QTableWidgetItem("Retención\nIVA"))
        self.tableWidget_xml.setHorizontalHeaderItem (12, QTableWidgetItem("Retención\nISR"))
        self.tableWidget_xml.setHorizontalHeaderItem (13, QTableWidgetItem("Total"))
        self.tableWidget_xml.setHorizontalHeaderItem (14, QTableWidgetItem("Forma\nPago"))
        self.tableWidget_xml.setHorizontalHeaderItem (15, QTableWidgetItem("Método\nPago"))



    def meDoblePicaronXML(self, row,column):
        print("me picaron en : " +str(row)+", " +str(column))
#         if column == 5:
#             suUUID = self.tableWidget_xml.item(row,2).text()
#             laFactura = None
#             for factura in self.listaDeFacturasOrdenadas:
#                 if factura.UUID == suUUID:
#                     print("i found it!")
#                     laFactura = factura
#
#                     break
#             mesage = ""
#             for concepto in laFactura.conceptos:
#                 mesage += concepto["descripcion"] + u'\n'
#
#             QtGui.QMessageBox.information(self, "Conceptos", mesage)
        if column == 2:


            xml =join(self.esteFolder + os.sep,self.tableWidget_xml.item(row, 2).text()+".xml")
            #acrobatPath = r'C:/Program Files (x86)/Adobe/Acrobat Reader DC/Reader/AcroRd32.exe'
            #subprocess.Popen("%s %s" % (acrobatPath, pdf))
            try:
                os.system('open %s' % xml)
                print("este guey me pico:"+xml)
            except:
                print ("el sistema no tiene una aplicacion por default para abrir xmls")
                QtGui.QMessageBox.information(self, "Information", "El sistema no tiene una aplicación por default para abrir xmls" )

        if column == 0:

            pdf = join(join(self.esteFolder,"pdfs"),self.tableWidget_xml.item(row, 2).text()+".pdf")
            #acrobatPath = r'C:/Program Files (x86)/Adobe/Acrobat Reader DC/Reader/AcroRd32.exe'
            #subprocess.Popen("%s %s" % (acrobatPath, pdf))
            try:
                #os.startfile(pdf)
                os.system('open %s' % pdf)
                print("este guey me pico:"+pdf)
            except:
                print ("el sistema no tiene una aplicacion por default para abrir pdfs")
                QtGui.QMessageBox.information(self, "Information", "El sistema no tiene una aplicación por default para abrir pdfs" )


    def meDoblePicaronResumen(self, row,column):
        print("me picaron en : " +str(row)+", " +str(column))
        pdf = join(join(self.esteFolder,"pdfs"),"resumenDiot.pdf")
        #acrobatPath = r'C:/Program Files (x86)/Adobe/Acrobat Reader DC/Reader/AcroRd32.exe'
        #subprocess.Popen("%s %s" % (acrobatPath, pdf))
        try:
            os.system('open %s' % pdf)
            print("este guey me pico:"+pdf)
        except:
            print ("el sistema no tiene una aplicacion por default para abrir pdfs")
            QtGui.QMessageBox.information(self, "Information", "El sistema no tiene una aplicación por default para abrir pdfs" )

    def cambiaSeleccionDeImpresora(self, curr, prev):
        print(curr.text())
        self.impresoraDefault = curr.text()
        #win32print.SetDefaultPrinter(self.impresoraDefault)

    def cambiaImpresora(self):
        # self.tabWidget.setCurrentIndex(1)
        self.listaDeImpresoras.setEnabled(True)

        #for (a,b,name,d) in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL):
        #    self.listaDeImpresoras.addItem(name)




    def imprime(self):
        #objetosMagicosOrdenados = sorted(self.objetosMagicos, key=lambda objetosMagicos: objetosMagicos.fecha)

        for factura in self.listaDeFacturasOrdenadas:
            try:
                if factura.total > 0:
                    print(factura.fechaTimbrado)
                    # hh = win32api.ShellExecute(0, "print", join(join(self.esteFolder,"pdfs"), factura.UUID+".pdf"),None, ".",  0)
                    # if hh > 40:
                    #     print("algo")
                    #     time_old.sleep(10)

                elif factura.total < 0:
                    print("negativo?????")
                else:#si es cero
                    print("nada")
            except:
                print("hay un pdf faltante o corrupto")


        #hh = win32api.ShellExecute(0, "print", join(join(self.esteFolder,"pdfs"), "resumenDiot.pdf") , None,  ".",  0)


    def esteItem(self, text, tooltip):
        item = QTableWidgetItem(text)
        item.setToolTip(tooltip)
        item.setFlags(item.flags() ^ Qt.ItemIsEditable)
        return item
    def cualCarpeta(self):
        self.folder.hide()
        esteFileChooser = QFileDialog()
        esteFileChooser.setFileMode(QFileDialog.Directory)
        if esteFileChooser.exec_():

            self.esteFolder = esteFileChooser.selectedFiles()[0] + "/"
            if not os.path.exists(join(self.esteFolder, "pdfs")):
                os.makedirs(join(self.esteFolder, "pdfs"))
            self.tableWidget_xml.clear()
            self.tableWidget_resumen.clear()
            self.tableWidget_resumen.repaint()
            self.ponEncabezado()
            self.tableWidget_xml.setRowCount(13)
            self.tableWidget_xml.repaint()
            cuantosDuplicados = 0
            self.listaDeDuplicados=[]
            self.listaDeFacturas = []
            self.listaDeUUIDs = []
            contador = 0
            for archivo in os.listdir(self.esteFolder):
                if ".xml" in archivo:

                    laFactura = Factura(join(self.esteFolder + os.sep,archivo))
                    if laFactura.version:
                        if laFactura.UUID in self.listaDeUUIDs:
                            print("no hagas nada")
                            cuantosDuplicados+=1
                            self.listaDeDuplicados.append(laFactura.UUID)
                        else:
                            self.listaDeUUIDs.append(laFactura.UUID)
                            contador += 1
                            self.listaDeFacturas.append(laFactura)

            if contador > 13:
                self.tableWidget_xml.setRowCount(contador)

            self.listaDeFacturasOrdenadas = sorted(self.listaDeFacturas, key=lambda listaDeFacturas: listaDeFacturas.fechaTimbrado)
            self.diccionarioPorRFCs = {}
            print(self.listaDeFacturasOrdenadas)


            pd =  QProgressDialog("Operation in progress.", "Cancel", 0, 100, self)
            pd.setWindowTitle("Huiini")
            pd.setValue(0)
            pd.show()

            if cuantosDuplicados > 0:
                mensaje = "hay "+str(cuantosDuplicados)+" duplicados\n"
                chunks = []
                for esteDuplicado in self.listaDeDuplicados:
                    chunks.append(str(esteDuplicado)+"\n")
                mensaje2 = "".join(chunks)
                mensaje = mensaje + mensaje2
                QtGui.QMessageBox.information(self, "Information", mensaje)

            contador = 0
            for factura in self.listaDeFacturasOrdenadas:
                pd.setValue(50*((contador + 1)/len(self.listaDeFacturasOrdenadas)))
                factura.setFolio(contador + 1)
                pd.setLabelText("Procesando: " + factura.UUID[:17] + "...")

                url = "http://huiini.pythonanywhere.com/upload"
                ####################################################Definir puerto  80 80   ################################
                xml_path = factura.xml_path

                #xml_path = 'C:/Users/SICAD/Dropbox/Araceli/2017/JUNIO/EGRESOS/DE820CD4-2F37-4751-9D38-0FD6947CB287.xml'
                files = {'files': open(xml_path , 'rb')}
                r = requests.post (url, files=files)
                # print(r.content)
                # print(r.text)
                xml_name = basename(factura.xml_path)
                url_get = "http://huiini.pythonanywhere.com/download"
                ###################################################Definir puerto 80 80, ip publica,  ################################

                if r.text == "ya":

                    r = requests.get(url_get, params={'uuid': factura.UUID, 'xml_name': xml_name, 'folio': contador + 1}, stream=True)
                    if r.status_code == 200:
                        with open(join(self.esteFolder, factura.UUID+'.pdf'),'wb') as f:
                            r.raw.decode_content = True
                            shutil.copyfileobj(r.raw, f)
                    else:
                        print("este no pude")
                self.tableWidget_xml.setItem(contador,1,self.esteItem(factura.fechaTimbrado,factura.fechaTimbrado))
                self.tableWidget_xml.setItem(contador,2,self.esteItem(factura.UUID,factura.UUID))
                self.tableWidget_xml.setItem(contador,3,self.esteItem(factura.ReceptorRFC,factura.ReceptorNombre))
                self.tableWidget_xml.setItem(contador,4,self.esteItem(factura.EmisorRFC,factura.EmisorNombre))
                mesage = ""
                for concepto in factura.conceptos:
                    mesage += concepto["descripcion"] + u'\n'
                self.tableWidget_xml.setItem(contador,5, self.esteItem(factura.conceptos[0]['descripcion'],mesage))
                self.tableWidget_xml.setItem(contador,6,self.esteItem(str(factura.version),""))
                self.tableWidget_xml.setItem(contador,7,self.esteItem(str(factura.subTotal),""))
                self.tableWidget_xml.setItem(contador,8,self.esteItem(str(factura.descuento),""))
                self.tableWidget_xml.setItem(contador,9,self.esteItem(str(factura.traslados["IVA"]["importe"]),""))
                self.tableWidget_xml.setItem(contador,10,self.esteItem(str(factura.traslados["IEPS"]["importe"]),""))
                self.tableWidget_xml.setItem(contador,11,self.esteItem(str(factura.retenciones["IVA"]),""))
                self.tableWidget_xml.setItem(contador,12,self.esteItem(str(factura.retenciones["ISR"]),""))
                self.tableWidget_xml.setItem(contador,13,self.esteItem(str(factura.total),""))
                self.tableWidget_xml.setItem(contador,14,self.esteItem(str(factura.formaDePago),""))
                self.tableWidget_xml.setItem(contador,15, self.esteItem(str(factura.metodoDePago),factura.metodoDePagoStr))

                if factura.EmisorRFC in self.diccionarioPorRFCs:
                    self.diccionarioPorRFCs[factura.EmisorRFC]['subTotal'] += float(factura.subTotal)
                    self.diccionarioPorRFCs[factura.EmisorRFC]['descuento'] += float(factura.descuento)
                    self.diccionarioPorRFCs[factura.EmisorRFC]['trasladoIVA'] += float(factura.traslados['IVA']['importe'])
                    self.diccionarioPorRFCs[factura.EmisorRFC]['importe'] += float(factura.subTotal)-float(factura.descuento)
                    self.diccionarioPorRFCs[factura.EmisorRFC]['total'] += float(factura.total)
                    print("sumale " + str(factura.subTotal) )
                else:
                    self.diccionarioPorRFCs[factura.EmisorRFC] = {'subTotal': float(factura.subTotal),
                                                                  'descuento': float(factura.descuento),
                                                                  'trasladoIVA': float(factura.traslados['IVA']['importe']),
                                                                  'importe': float(factura.subTotal)-float(factura.descuento),
                                                                  'total': float(factura.total)
                                                                }
                    print("crealo con " + str(factura.subTotal))
                contador +=1

            #if contador == len(self.listaDeFacturasOrdenadas):
            pd.setLabelText("Creando Resumen...")
            for t in range(0,5):
                time_old.sleep(0.2*len(self.listaDeFacturasOrdenadas))
                pd.setValue(pd.value() + ( (100 - pd.value()) / 2))

            contador = -1
            for factura in self.listaDeFacturasOrdenadas:
                try:
                    contador += 1
                    if os.path.isfile(join(self.esteFolder,factura.UUID+".pdf")):

                        self.tableWidget_xml.setCellWidget(contador,0, ImgWidget1(self))
                    else:
                        self.tableWidget_xml.setCellWidget(contador,0, ImgWidget2(self))

                except:
                    print("no pude un xml")

            self.imprimir.setEnabled(True)

            self.numeroDeFacturasValidas = len(self.listaDeFacturasOrdenadas)


            self.sumale()
            pd.setLabelText("Carpeta procesada")
            pd.setValue(pd.value() + ( (100 - pd.value()) / 2))
            self.hazResumenDiot(self.esteFolder)
            pd.setValue(100)
            self.tableWidget_resumen.setItem(0,1,QTableWidgetItem("Resumen Diot"))
            self.tableWidget_resumen.setItem(0,2,QTableWidgetItem("Sumatoria del Periodo"))
            self.tableWidget_resumen.setCellWidget(0,0, ImgWidget1(self))

            for factura in self.listaDeFacturasOrdenadas:
                esteFile = factura.UUID + ".pdf"
                try:
                    if os.path.exists(os.path.join(os.path.join(self.esteFolder,"pdfs"),esteFile)):
                        os.remove(os.path.join(os.path.join(self.esteFolder,"pdfs"),esteFile))
                    os.rename(os.path.join(self.esteFolder,esteFile), os.path.join(os.path.join(self.esteFolder,"pdfs"),esteFile))
                except:
                    QtGui.QMessageBox.information(self, "Information", "No fue posible mover " + esteFile)

            try:
                if os.path.exists(os.path.join(os.path.join(self.esteFolder,"pdfs"),"resumenDiot.pdf")):
                    os.remove(os.path.join(os.path.join(self.esteFolder,"pdfs"),"resumenDiot.pdf"))
                os.rename(os.path.join(self.esteFolder,"resumenDiot.pdf"), os.path.join(os.path.join(self.esteFolder,"pdfs"),"resumenDiot.pdf"))
            except:
                QtGui.QMessageBox.information(self, "Information", "No fue posible mover resumenDiot.pdf")

            for esteFile in listdir(self.esteFolder):
                if esteFile.endswith(".tex") or esteFile.endswith(".aux") or esteFile.endswith(".log"):
                    print("aqui borraria")
                    try:
                        os.remove(join(self.esteFolder,esteFile))
                    except:
                        QtGui.QMessageBox.information(self, "Information", "No fue posible borrar " + join(self.esteFolder,esteFile))

            #obtener los warnings de las facturas
            mensajeAlerta =""
            for factura in self.listaDeFacturasOrdenadas:
                if not factura.mensaje == "":
                    mensajeAlerta += factura.UUID + factura.mensaje + r'\n'
            if not mensajeAlerta == "":
                QtGui.QMessageBox.information(self, "Information", mensajeAlerta)
            #time_old.sleep(1)

            pd.hide()


        self.folder.setText("Carpeta Procesada: " + u'\n' + self.esteFolder)
        self.folder.show()
        self.raise_()
        self.activateWindow()

app = QApplication(sys.argv)
form = Ui_MainWindow()
form.show()

app.exec_()
