#-*- encoding: utf-8 -*-
from PySide.QtCore import *
import requests
from PySide.QtCore import Qt
from PySide.QtGui import *
from PySide import QtGui, QtCore
import sys
import guiV2
from os import listdir
from os.path import isfile, join, basename
import shutil
import os
import win32print
import win32api
import time as time_old
from subprocess import Popen
from FacturasClient import FacturaClient as Factura
import math
import json
from requests.auth import HTTPBasicAuth
from datetime import datetime
import hashlib
import descarga



##pyside-uic mainwindow.ui -o gui.py
##pyside-uic mainwindowV2.ui -o guiV2.py
# class checaMe(requests.auth.AuthBase):
#     def __call__(self, r):
#         # Implement my authentication
#         return r

#url_server = "http://192.168.15.17:8008"
url_server = "http://huiini.pythonanywhere.com"


try:
    scriptDirectory = os.path.dirname(os.path.abspath(__file__))
except NameError:  # We are the main py2exe script, not a module
    scriptDirectory = os.path.dirname(os.path.abspath(sys.argv[0]))




class ImgWidgetPalomita(QtGui.QLabel):

    def __init__(self, parent=None):
        super(ImgWidgetPalomita, self).__init__(parent)
        pic_palomita = QtGui.QPixmap(join(scriptDirectory,"palomita.png"))
        self.setPixmap(pic_palomita)

class ImgWidgetTache(QtGui.QLabel):

    def __init__(self, parent=None):
        super(ImgWidgetTache, self).__init__(parent)
        pic_tache = QtGui.QPixmap(join(scriptDirectory,"x.png"))
        self.setPixmap(pic_tache)



class Ui_MainWindow(QMainWindow, guiV2.Ui_MainWindow):

    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__(parent)
        self.setupUi(self)

        print(scriptDirectory)
        logoPix = QtGui.QPixmap(join(scriptDirectory,"logo.png"))
        self.labelLogo.setPixmap(logoPix)
        self.pdflatex_path = "C:/Program Files/MiKTeX 2.9/miktex/bin/x64/pdflatex.exe"

        self.carpetaChooser.clicked.connect(self.cualCarpeta)
        self.descarga_bt.clicked.connect(self.descarga_mesta)
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

        #url_get = "http://huiini.pythonanywhere.com/resumen"
        url_get =  "%s/resumen/%s/" % (url_server, self.hash_carpeta)

        r = requests.get(url_get, stream=True,
                        auth=(self.w.username.text(), self.w.password.text()))
        time_old.sleep(1)
        if r.status_code == 200:
            with open(join(join(self.esteFolder,"huiini"), 'resumenDiot.xlsx'),'wb') as f:
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

        url_get =  "%s/remove/%s/%s" % (url_server, self.hash_carpeta, elNombre)

        r = requests.get(url_get, stream=True,
                        auth=(self.w.username.text(), self.w.password.text()))


        self.hazResumenDiot(self.esteFolder)
        # try:
        #     if os.path.exists(os.path.join(os.path.join(self.esteFolder,"huiini"),"resumenDiot.pdf")):
        #
        #         os.remove(os.path.join(os.path.join(self.esteFolder,"huiini"),"resumenDiot.pdf"))
        #
        #     os.rename(os.path.join(self.esteFolder,"resumenDiot.pdf"), os.path.join(os.path.join(self.esteFolder,"huiini"),"resumenDiot.pdf"))
        # except:
        #     QtGui.QMessageBox.information(self, "Information", "tienes abierto el resumenDiot.pdf")


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
            self.tableWidget_resumen.setCellWidget(1,0,ImgWidgetPalomita(self))
            self.tableWidget_resumen.setCellWidget(0,0,ImgWidgetTache(self))


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
                os.startfile(xml)
                print("este guey me pico:"+xml)
            except:
                print ("el sistema no tiene una aplicacion por default para abrir xmls")
                QtGui.QMessageBox.information(self, "Information", "El sistema no tiene una aplicación por default para abrir xmls" )

        if column == 0:

            pdf = join(join(self.esteFolder,"huiini"),self.tableWidget_xml.item(row, 2).text()+".pdf")
            #acrobatPath = r'C:/Program Files (x86)/Adobe/Acrobat Reader DC/Reader/AcroRd32.exe'
            #subprocess.Popen("%s %s" % (acrobatPath, pdf))
            try:
                os.startfile(pdf)
                print("este guey me pico:"+pdf)
            except:
                print ("el sistema no tiene una aplicacion por default para abrir pdfs")
                QtGui.QMessageBox.information(self, "Information", "El sistema no tiene una aplicación por default para abrir pdfs" )


    def meDoblePicaronResumen(self, row,column):
        print("me picaron en : " +str(row)+", " +str(column))
        pdf = join(join(self.esteFolder,"huiini"),"resumenDiot.pdf")
        #acrobatPath = r'C:/Program Files (x86)/Adobe/Acrobat Reader DC/Reader/AcroRd32.exe'
        #subprocess.Popen("%s %s" % (acrobatPath, pdf))
        try:
            os.startfile(pdf)
            print("este guey me pico:"+pdf)
        except:
            print ("el sistema no tiene una aplicacion por default para abrir pdfs")
            QtGui.QMessageBox.information(self, "Information", "El sistema no tiene una aplicación por default para abrir pdfs" )

    def cambiaSeleccionDeImpresora(self, curr, prev):
        print(curr.text())
        self.impresoraDefault = curr.text()
        win32print.SetDefaultPrinter(self.impresoraDefault)

    def cambiaImpresora(self):
        # self.tabWidget.setCurrentIndex(1)
        self.listaDeImpresoras.setEnabled(True)

        for (a,b,name,d) in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL):
            self.listaDeImpresoras.addItem(name)




    def imprime(self):
        #objetosMagicosOrdenados = sorted(self.objetosMagicos, key=lambda objetosMagicos: objetosMagicos.fecha)

        for factura in self.listaDeFacturasOrdenadas:
            try:
                if factura.total > 0:
                    print(factura.fechaTimbrado)
                    hh = win32api.ShellExecute(0, "print", join(join(self.esteFolder,"huiini"), factura.UUID+".pdf"),None, ".",  0)
                    if hh > 40:
                        print("algo")
                        time_old.sleep(10)

                elif factura.total < 0:
                    print("negativo?????")
                else:#si es cero
                    print("nada")
            except:
                print("hay un pdf faltante o corrupto")


        hh = win32api.ShellExecute(0, "print", join(join(self.esteFolder,"huiini"), "resumenDiot.pdf") , None,  ".",  0)
    def esteItem(self, text, tooltip):
        item = QTableWidgetItem(text)
        item.setToolTip(tooltip)
        item.setFlags(item.flags() ^ Qt.ItemIsEditable)
        return item


    def hazPDFs(self):
        contador = -1
        for factura in self.listaDeFacturasOrdenadas:
            contador += 1
            if factura.has_pdf == False:
                xml_name = basename(factura.xml_path)
                factura.conviertemeEnTex()
                factura.conviertemeEnPDF()


                factura.has_pdf = True
                self.tableWidget_xml.setCellWidget(contador,0, ImgWidgetPalomita(self))

                #     else:
                #         self.tableWidget_xml.setCellWidget(contador,0, ImgWidgetTache(self))
                # except:
                #     self.tableWidget_xml.setCellWidget(contador,0, ImgWidgetTache(self))


    def cualCarpeta(self):

        self.folder.hide()
        esteFileChooser = QFileDialog()
        esteFileChooser.setFileMode(QFileDialog.Directory)
        if esteFileChooser.exec_():

            self.esteFolder = esteFileChooser.selectedFiles()[0] + "/"
            pre_hash = self.esteFolder + str(datetime.now())
            pal_hash = pre_hash.encode('utf-8')
            self.hash_carpeta = hashlib.sha224(pal_hash).hexdigest()

            if not os.path.exists(join(self.esteFolder, "huiini")):
                os.makedirs(join(self.esteFolder, "huiini"))
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

                #url = "http://huiini.pythonanywhere.com/upload"
                #url =  "%s/upload/%s/" % (url_server, self.hash_carpeta)

                ####################################################Definir puerto  80 80   ################################
                xml_path = factura.xml_path

                #xml_path = 'C:/Users/SICAD/Dropbox/Araceli/2017/JUNIO/EGRESOS/DE820CD4-2F37-4751-9D38-0FD6947CB287.xml'
                files = {'files': open(xml_path , 'rb')}
                # print(r.content
                # print(r.text)


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
                self.tableWidget_xml.setItem(contador,14,self.esteItem(factura.formaDePago,""))
                self.tableWidget_xml.setItem(contador,15, self.esteItem(factura.metodoDePago,factura.metodoDePagoStr))

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

                # try:
                #     r = requests.post (url, files=files,
                #                        timeout=20,
                #                        data={'folio' :contador + 1},
                #                        auth=(self.w.username.text(), self.w.password.text()))
                # except:
                #     continue


            #if contador == len(self.listaDeFacturasOrdenadas):
            pd.setLabelText("Creando Resumen...")
            for t in range(0,5):
                time_old.sleep(0.05*len(self.listaDeFacturasOrdenadas))
                pd.setValue(pd.value() + ( (100 - pd.value()) / 2))




            self.hazPDFs()



            contador = -1

            # time_old.sleep(0.5*len(self.listaDeFacturasOrdenadas))

            self.imprimir.setEnabled(True)

            self.numeroDeFacturasValidas = len(self.listaDeFacturasOrdenadas)


            self.sumale()
            pd.setLabelText("Carpeta procesada")
            pd.setValue(pd.value() + ( (100 - pd.value()) / 2))
            self.hazResumenDiot(self.esteFolder)
            pd.setValue(100)
            self.tableWidget_resumen.setItem(0,1,QTableWidgetItem("Resumen Diot"))
            self.tableWidget_resumen.setItem(0,2,QTableWidgetItem("Sumatoria del Periodo"))
            self.tableWidget_resumen.setCellWidget(0,0, ImgWidgetPalomita(self))

            #obtener los warnings de las facturas
            mensajeAlerta =""
            for factura in self.listaDeFacturasOrdenadas:
                if not factura.mensaje == "":
                    mensajeAlerta += factura.UUID + factura.mensaje + r'\n'
            if not mensajeAlerta == "":
                QtGui.QMessageBox.information(self, "Information", mensajeAlerta)

            pd.hide()


        self.folder.setText("Carpeta Procesada: " + u'\n' + self.esteFolder)
        self.folder.show()
        self.raise_()
        self.activateWindow()

app = QApplication(sys.argv)
form = Ui_MainWindow()
form.show()
form.doit()

app.exec_()
