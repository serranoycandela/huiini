#-*- encoding: utf-8 -*-
from PySide2.QtCore import *
from PySide2.QtCore import Qt, QDir
from PySide2.QtGui import *
from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtWidgets import QLineEdit, QTableWidgetItem, QFileDialog, QProgressDialog, QMessageBox, QListView, QAbstractItemView, QTreeView, QDialog, QVBoxLayout, QDialogButtonBox, QFileSystemModel, QInputDialog
from PySide2.QtWidgets import QPushButton, QListWidget, QListWidgetItem
import sys
import guiV2
from os import listdir, environ
from os.path import isfile, join, basename
import shutil
import os
import win32print
import win32api
import time as time_old
from subprocess import Popen
from FacturasLocal import FacturaLocal as Factura
import math
import json
#import xlsxwriter
from openpyxl.utils.dataframe import dataframe_to_rows
import pandas as pd

from openpyxl import load_workbook,  Workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Border, Side, PatternFill, Font, Alignment, numbers
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter


from datetime import datetime
from copy import copy
import ghostscript
import locale



##C:\Python36\Scripts\pyside2-uic.exe mainwindowV2.ui -o guiV2.py
##C:\Python36\Scripts\pyinstaller.exe huiini.py





try:
    scriptDirectory = os.path.dirname(os.path.abspath(__file__))
except NameError:  # We are the main py2exe script, not a module
    scriptDirectory = os.path.dirname(os.path.abspath(sys.argv[0]))

class categorias_widget(QDialog):
    def __init__(self, parent=None):
        super(categorias_widget, self).__init__(parent)
        self.setMinimumSize(520, 850)
        layout = QVBoxLayout()
        self.add_button = QPushButton("Nueva")
        layout.addWidget(self.add_button)
        self.edit_button = QPushButton("Editar")
        layout.addWidget(self.edit_button)
        self.remove_button = QPushButton("Eliminar")
        layout.addWidget(self.remove_button)
        self.myListWidget = QListWidget()
        layout.addWidget(self.myListWidget)
        self.setLayout(layout)


class getFilesDlg(QDialog):

    # sendPaths is a signal emitted by getPaths containing a list of file paths from
    # the users selection via this dialog.
    sendPaths = Signal(list)

    def __init__(self, parent=None):
        super(getFilesDlg, self).__init__(parent)

        self.setMinimumSize(520,850)

        self.fileDlgPaths = []

        layout = QVBoxLayout()

        self.btnBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        self.btnBox.accepted.connect(self.getPaths)
        self.btnBox.rejected.connect(self.close)

        self.fsModel = QFileSystemModel()
        self.fsModel.setFilter(QtCore.QDir.AllDirs | QtCore.QDir.NoDotAndDotDot)

        self.treeView = QTreeView()
        self.treeView.setSelectionMode(QTreeView.ExtendedSelection)

        self.treeView.setModel(self.fsModel)
        self.treeView.setColumnWidth(0, 361)
        self.treeView.setColumnHidden(1, True)
        self.treeView.setColumnHidden(2, True)
        self.fsModel.setRootPath("")
        self.treeView.setSortingEnabled(True)
        layout.addWidget(self.treeView)
        layout.addWidget(self.btnBox)
        self.setLayout(layout)
        self.treeView.setRootIndex(self.fsModel.index(""))
        home = os.path.expanduser('~')
        pdflatex_folder_path = os.path.join(home, 'Documents', 'huiini')
        self.huiini_home_folder_path = ""
        if os.path.exists(os.path.join(pdflatex_folder_path,"huiini_home_folder_path.txt")):
            with open(os.path.join(pdflatex_folder_path,"huiini_home_folder_path.txt")) as f:
                self.huiini_home_folder_path = f.readline()
        print(self.huiini_home_folder_path)


        path_restante = self.huiini_home_folder_path
        while path_restante != os.path.split(path_restante)[0]:
            index_previo = self.fsModel.index(path_restante)
            self.treeView.expand(index_previo)
            path_restante = os.path.split(path_restante)[0]
        index_previo = self.fsModel.index(path_restante)
        self.treeView.expand(index_previo)

        # self.treeView.setRootIndex(self.fsModel.index("C:\\Dropbox"))
        # self.treeView.expand(self.treeView.rootIndex())
        #self.fsModel.setRootPath(environ['HOMEPATH'])
        # self.treeView.setRootIndex(self.fsModel.index("\\"))
        #self.treeView.expand(self.treeView.rootIndex())


    def getPaths(self):
    	# For some reason duplicates were being returned when they weren't supposed to.
    	# This obtains the selected files from the dialog and only returns individual
    	# paths.
    	indexes = self.treeView.selectedIndexes()
    	if indexes:
    		self.fileDlgPaths = []
    		for i in indexes:

    			# Possible permission error occuring here
    			# unable to replicate at this time
    			path = self.fsModel.filePath(i)
    			if path not in self.fileDlgPaths:
    				self.fileDlgPaths.append(path)
    		self.close() # To close the dialog on an accept signal
    		self.sendPaths.emit(self.fileDlgPaths)

class ImgWidgetPalomita(QtWidgets.QLabel):

    def __init__(self, parent=None):
        super(ImgWidgetPalomita, self).__init__(parent)
        pic_palomita = QtGui.QPixmap(join(scriptDirectory,"palomita.png"))
        self.setPixmap(pic_palomita)

class ImgWidgetTache(QtWidgets.QLabel):

    def __init__(self, parent=None):
        super(ImgWidgetTache, self).__init__(parent)
        pic_tache = QtGui.QPixmap(join(scriptDirectory,"x.png"))
        self.setPixmap(pic_tache)



class Ui_MainWindow(QtWidgets.QMainWindow, guiV2.Ui_MainWindow):

    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__(parent)
        self.setupUi(self)

        print(scriptDirectory)
        logoPix = QtGui.QPixmap(join(scriptDirectory,"logo.png"))
        self.labelLogo.setPixmap(logoPix)
        self.pdflatex_path = "C:/Program Files/MiKTeX 2.9/miktex/bin/x64/pdflatex.exe"

        self.carpetaChooser.clicked.connect(self.cualCarpeta)
        self.agrega_cats.clicked.connect(self.edita_categorias)
        #self.descarga_bt.clicked.connect(self.descarga_mesta)
        self.imprimir.clicked.connect(self.imprime)

        self.impresora.clicked.connect(self.cambiaImpresora)
        self.botonCancela.clicked.connect(self.cancelaImpresion)

        self.listaDeImpresoras.currentItemChanged.connect(self.cambiaSeleccionDeImpresora)

        self.tableWidget_xml.setColumnCount(15)
        self.tableWidget_xml.setColumnWidth(0,30)#pdf
        self.tableWidget_xml.setColumnWidth(1,95)#fecha
        self.tableWidget_xml.setColumnWidth(2,70)#uuid
        self.tableWidget_xml.setColumnWidth(3,120)#receptor-nombre
        self.tableWidget_xml.setColumnWidth(4,120)#emisor-rfc
        self.tableWidget_xml.setColumnWidth(5,120)#concepto
        self.tableWidget_xml.setColumnWidth(6,75)#Subtotal
        self.tableWidget_xml.setColumnWidth(7,80)#Descuento
        self.tableWidget_xml.setColumnWidth(8,80)#traslados-iva
        self.tableWidget_xml.setColumnWidth(9,80)#traslados-ieps
        self.tableWidget_xml.setColumnWidth(10,75)#retIVA
        self.tableWidget_xml.setColumnWidth(11,75)#retISR
        self.tableWidget_xml.setColumnWidth(12,80)#total
        self.tableWidget_xml.setColumnWidth(13,74)#formaDePago
        self.tableWidget_xml.setColumnWidth(14,77)#metodoDePago

        self.tableWidget_xml.verticalHeader().setFixedWidth(35)

        self.tableWidget_resumen.setColumnCount(10)
        self.tableWidget_resumen.setColumnWidth(0,30)
        self.tableWidget_resumen.setColumnWidth(1,122)
        self.tableWidget_resumen.setColumnWidth(2,176)
        self.tableWidget_resumen.setColumnWidth(3,75)
        self.tableWidget_resumen.setColumnWidth(4,80)
        self.tableWidget_resumen.setColumnWidth(5,80)
        self.tableWidget_resumen.setColumnWidth(6,80)
        self.tableWidget_resumen.setColumnWidth(7,75)
        self.tableWidget_resumen.setColumnWidth(8,75)
        self.tableWidget_resumen.setColumnWidth(9,80)
        self.tableWidget_resumen.setRowCount(2)
        #self.tableWidget_resumen.verticalHeader().setFixedWidth(35)

        header = self.tableWidget_xml.verticalHeader()
        header.setContextMenuPolicy(Qt.CustomContextMenu)
        header.customContextMenuRequested.connect(self.handleHeaderMenu)

        lc = ["Pdf","Fecha","UUID","Receptor","Emisor","Concepto","Subtotal","Descuento","Traslado\nIVA","Traslado\nIEPS","Retención\nIVA","Retención\nISR","Total","Forma\nPago","Método\nPago"]
        self.ponEncabezado(lc)

        self.tableWidget_xml.cellDoubleClicked.connect(self.meDoblePicaronXML)
        self.tableWidget_resumen.cellDoubleClicked.connect(self.meDoblePicaronResumen)
        self.progressBar.hide()
        self.tableWidget_xml.horizontalHeader().sectionClicked.connect(self.reordena)


    def reordena(self, column):
        print("reodenaria")
        if column == 2:
            print("reodenaria con uuid")
            self.listaDeFacturasOrdenadas = sorted(self.listaDeFacturasOrdenadas, key=lambda listaDeFacturasOrdenadas: listaDeFacturasOrdenadas.UUID)

    def quitaCategoria(self):
        curr_indexes = self.cats_dialog.myListWidget.selectedIndexes()
        if len(curr_indexes)>1:
            print("no")
        else:
            #confirmacion para maricas
            self.lista_ordenada.pop(curr_indexes[0].row())
            with open(self.json_path, "w", encoding="utf-8") as jsonfile:
                json.dump(self.lista_ordenada, jsonfile)

            self.cats_dialog.myListWidget.takeItem(curr_indexes[0].row())

    def editaCategoria(self):
        curr_indexes = self.cats_dialog.myListWidget.selectedIndexes()
        if len(curr_indexes)>1:
            print("no")
        else:

            nombre, ok = QInputDialog().getText(self.cats_dialog, "Nombre de la Categoría",
                                        "Nombre de la categoría:", QLineEdit.Normal,self.lista_ordenada[curr_indexes[0].row()][1])
            claves_ps, ok = QInputDialog().getText(self.cats_dialog, "Lista de claves de producto o servicio",
                                         "clave_ps:", QLineEdit.Normal,
                                         self.lista_ordenada[curr_indexes[0].row()][0])

            self.lista_ordenada[curr_indexes[0].row()][0] = claves_ps
            self.lista_ordenada[curr_indexes[0].row()][1] = nombre
            self.lista_ordenada = sorted(self.lista_ordenada, key=lambda tup: tup[1])
            with open(self.json_path, "w", encoding="utf-8") as jsonfile:
                json.dump(self.lista_ordenada, jsonfile)
            self.cats_dialog.myListWidget.clear()
            for tupla in self.lista_ordenada:
                self.cats_dialog.myListWidget.addItem(tupla[1]+" ("+tupla[0]+")")


    def agregaCategoria(self):
        nombre, ok = QInputDialog().getText(self.cats_dialog, "Nombre de la Categoría",
                                     "Nombre de la categoría:", QLineEdit.Normal,"")
        claves_ps, ok = QInputDialog().getText(self.cats_dialog, "Lista de claves de producto o servicio",
                                     "clave_ps:", QLineEdit.Normal,
                                     "")
        claves_ps.strip()


        for clave in claves_ps.split(","):
            pasa = True
            for tupla in self.lista_ordenada:
                if tupla[0].startswith(clave) or clave.startswith(tupla[0]):
                    pasa = False
                    QMessageBox.information(self, "Advertencia", "La inicio de clave " + clave + " ya está considerado en la categoría " + tupla[1])
            if pasa:
                if clave == "" or nombre == "":
                    print("no mames")
                else:
                    self.lista_ordenada.append([clave, nombre])

        self.lista_ordenada = sorted(self.lista_ordenada, key=lambda tup: tup[1])
        with open(self.json_path, "w", encoding="utf-8") as jsonfile:
            json.dump(self.lista_ordenada, jsonfile)
        self.cats_dialog.myListWidget.clear()
        for tupla in self.lista_ordenada:
            self.cats_dialog.myListWidget.addItem(tupla[1]+" ("+tupla[0]+")")


    def edita_categorias(self):
        self.cats_dialog = categorias_widget()
        self.cats_dialog.remove_button.clicked.connect(self.quitaCategoria)
        self.cats_dialog.add_button.clicked.connect(self.agregaCategoria)
        self.cats_dialog.edit_button.clicked.connect(self.editaCategoria)
        folder_cliente = os.path.split(os.path.split(self.paths[0])[0])[0]
        self.json_path = join(folder_cliente, "categorias_huiini.json")
        if os.path.exists(self.json_path):
            with open(self.json_path, "r", encoding="utf-8") as jsonfile:
                lista_de_tuplas = json.load(jsonfile)
        else:
            lista_de_tuplas = []


        # lista_de_tuplas.extend(lista_categorias_default)
        self.lista_ordenada = sorted(lista_de_tuplas, key=lambda tup: tup[1])
        for tupla in self.lista_ordenada:
            i = QListWidgetItem(tupla[1]+" ("+tupla[0]+")")
            # if "Default" in tupla[0]:
            #     i.setBackground(QtGui.QColor("#ababab"))
            self.cats_dialog.myListWidget.addItem(i)
        self.cats_dialog.exec()
        # folder_cliente = os.path.split(os.path.split(self.paths[0])[0])[0]
        # json_path = join(folder_cliente,"categorias_huiini.json")
        # if os.path.exists(json_path):
        #     with open(json_path, "r") as jsonfile:
        #         lista_de_tuplas = json.load(jsonfile)
        # else:
        #     lista_de_tuplas = []
        #
        #
        #
        # nombre, ok = QInputDialog().getText(self, "Nombre de la Categoría",
        #                              "Nombre de la categoría:", QLineEdit.Normal,
        #                              QDir().home().dirName())
        # claves_ps, ok = QInputDialog().getText(self, "Lista de claves de producto o servicio",
        #                              "clave_ps:", QLineEdit.Normal,
        #                              QDir().home().dirName())
        #
        # claves_ps.strip()
        #
        # for clave in claves_ps.split(","):
        #     lista_de_tuplas.append([clave,nombre])
        # with open(json_path, "w") as jsonfile:
        #     json.dump(lista_de_tuplas, jsonfile)





    def as_text(self,value):
        if value is None:
            return ""
        return str(value)

    def style_ws(self, ws, columna_totales, sumas_row):
        cell_border = Border(left=Side(border_style='medium', color='FF000000'),
                     right=Side(border_style='medium', color='FF000000'),
                     top=Side(border_style='medium', color='FF000000'),
                     bottom=Side(border_style='medium', color='FF000000'))

        cell_border_sumas = Border(left=Side(border_style=None, color='FF000000'),
                     right=Side(border_style=None, color='FF000000'),
                     top=Side(border_style='thin', color='FF000000'),
                     bottom=Side(border_style='thin', color='FF000000'))

        for cell in ws["1:1"]:
            cell.fill = PatternFill(start_color="8ccbff", end_color="8ccbff", fill_type = "solid")
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
            cell.border = cell_border

        for column_cells in ws.columns:
            #length = max(len(self.as_text(cell.value)) for cell in column_cells)
            length = len(self.as_text(column_cells[0].value))
            ws.column_dimensions[column_cells[0].column_letter].width = length+5

        ws.column_dimensions['A'].width = 12

        for cell in ws['A']:
            cell.font = Font(bold=True)


        for cell in ws[str(sumas_row)+":"+str(sumas_row)]:
            cell.border = cell_border_sumas
            cell.font = Font(bold=True)


        for i in range(2,sumas_row+1):
            for j in range(2,columna_totales+1):
                ws.cell(i,j).number_format = numbers.FORMAT_NUMBER_COMMA_SEPARATED1

        ws.cell(sumas_row,1).fill = PatternFill(start_color="4ac6ff", end_color="4ac6ff", fill_type = "solid")
        ws.cell(sumas_row,1).border = cell_border

    def style_ws_ingresos(self, ws, columna_totales, sumas_row):
        cell_border = Border(left=Side(border_style=None, color='FF000000'),
                     right=Side(border_style=None, color='FF000000'),
                     top=Side(border_style='medium', color='FF000000'),
                     bottom=Side(border_style='medium', color='FF000000'))

        cell_border_sumas = Border(left=Side(border_style=None, color='FF000000'),
                     right=Side(border_style=None, color='FF000000'),
                     top=Side(border_style='thin', color='FF000000'),
                     bottom=Side(border_style='thin', color='FF000000'))

        for column in range(1,18):
            cell = ws.cell(1,column)
            cell.fill = PatternFill(start_color="8ccbff", end_color="8ccbff", fill_type = "solid")
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
            cell.border = cell_border

        for column_cells in ws.columns:
            #length = max(len(self.as_text(cell.value)) for cell in column_cells)
            length = len(self.as_text(column_cells[0].value))
            ws.column_dimensions[column_cells[0].column_letter].width = length+5

        ws.column_dimensions['A'].width = 12

        # for cell in ws['A']:
        #     cell.font = Font(bold=True)



        for column in range(1,18):
            cell = ws.cell(sumas_row,column)
            cell.border = cell_border_sumas
            cell.font = Font(bold=True)


        for i in range(2,sumas_row+1):
            for j in range(8,14):
                ws.cell(i,j).number_format = numbers.FORMAT_NUMBER_COMMA_SEPARATED1

        for column in range(20,27):
            cell = ws.cell(3,column)
            cell.fill = PatternFill(start_color="8ccbff", end_color="8ccbff", fill_type = "solid")
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
            cell.border = cell_border
            cell = ws.cell(20,column)
            cell.fill = PatternFill(start_color="8ccbff", end_color="8ccbff", fill_type = "solid")
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
            cell.border = cell_border

        for column in range(20,27):
            cell = ws.cell(16,column)
            cell.border = cell_border_sumas
            cell.font = Font(bold=True)
            cell = ws.cell(33,column)
            cell.border = cell_border_sumas
            cell.font = Font(bold=True)

        ws.column_dimensions['T'].width = 12
        ws.column_dimensions['U'].width = 12
        ws.column_dimensions['V'].width = 12
        ws.column_dimensions['W'].width = 12
        ws.column_dimensions['X'].width = 12
        ws.column_dimensions['Y'].width = 12
        ws.column_dimensions['Z'].width = 12



    def calculaAgregados(self, df, ws_cats, variable):

        por_categorias = df.groupby(['mes', 'tipo'], as_index=False).agg({variable:sum})
        por_categorias_wide = por_categorias.pivot_table(index="mes",columns=['tipo'],values=variable,fill_value= 0)
        por_categorias_wide.reset_index(inplace=True)
        por_categorias_wide['mes'] = pd.Categorical(por_categorias_wide['mes'], self.todos_los_meses)
        por_categorias_wide = por_categorias_wide.sort_values("mes")
        por_categorias_wide['mes'] = por_categorias_wide.mes.astype(str)
        for r in dataframe_to_rows(por_categorias_wide, index=False, header=True):
            ws_cats.append(r)
        #print(por_categorias_wide)

        if variable == "importeConcepto":
            col_sum = "H"

        if variable == "impuestos":
            col_sum = "I"



        self.numeroDeColumnas = len(por_categorias_wide.columns)
        self.columna_totales = self.numeroDeColumnas + 1
        self.sumas_row = len(por_categorias_wide.index)+2
        ws_cats.cell(1,self.columna_totales, "Total")
        ws_cats.cell(self.sumas_row,1,"Anual")

        for i in range(2,self.columna_totales):
            letra = get_column_letter(i)
            for j in range(2,self.sumas_row):
                ws_cats.cell(j,i,"=SUMIFS(Conceptos!"+col_sum+":"+col_sum+",Conceptos!K:K,"+letra+"1,Conceptos!A:A,A"+str(j)+',Conceptos!L:L,"Pagado")')



        for i in range(2,self.columna_totales):
            letra = get_column_letter(i)
            ws_cats.cell(self.sumas_row,i,"=SUM("+letra+ "2:"+letra+ str(self.sumas_row-1)+")")

        letra_final = get_column_letter(self.numeroDeColumnas)
        for i in range(2,self.sumas_row):
            ws_cats.cell(i,self.columna_totales,"=SUM(B"+str(i)+ ":"+letra_final+ str(i)+")")

        letra_sumas = get_column_letter(self.columna_totales)
        ws_cats.cell(self.sumas_row,self.columna_totales,"=SUM("+letra_sumas+"2:"+letra_sumas+str(self.sumas_row-1)  +")")

    def hazTabDeIngresos(self,paths):
        if len(self.listaDeFacturasIngresos) > 0:
            workbook = load_workbook(self.annual_xlsx_path)
            if not "Ingresos" in workbook.sheetnames:
                ws_ingresos = workbook.create_sheet("Ingresos")

            ws_ingresos.cell(1, 1, "MesEmision")
            ws_ingresos.cell(1, 2,     "MesPago")
            ws_ingresos.cell(1, 3,     "uuid")
            ws_ingresos.cell(1, 4,     "FECHA")
            ws_ingresos.cell(1, 5,     "RFC (Receptor)")
            ws_ingresos.cell(1, 6,     "RAZON SOCIAL")
            ws_ingresos.cell(1, 7,     "DESCRIPCION")
            ws_ingresos.cell(1, 8,     "SUBTOTAL")
            ws_ingresos.cell(1, 9,     "I.V.A.")
            ws_ingresos.cell(1, 10,     "IMPORTE")
            ws_ingresos.cell(1, 11,     "RET ISR")
            ws_ingresos.cell(1, 12,     "RET IVA")
            ws_ingresos.cell(1, 13,     "T O T A L")
            ws_ingresos.cell(1, 14,     "M-Pago")
            ws_ingresos.cell(1, 15,     "Status")
            ws_ingresos.cell(1, 16,     "complementosDePago")
            ws_ingresos.cell(1, 17,     "Tipo")


            row = 1
            dv = DataValidation(type="list", formula1='"Pendiente,Pagado"', allowBlank=True)
            ws_ingresos.add_data_validation(dv)
            dv_mes = DataValidation(type="list", formula1='"ENERO,FEBRERO,MARZO,ABRIL,MAYO,JUNIO,JULIO,AGOSTO,SEPTIEMBRE,OCTUBRE,NOVIEMBRE,DICIEMBRE,--"', allow_blank=True)
            ws_ingresos.add_data_validation(dv_mes)

            for factura in self.listaDeFacturasIngresos:

                row += 1
                numeroDeMes = int(factura.fechaTimbrado.split("-")[1])
                dv_mes.add(ws_ingresos.cell(row, 1))
                dv_mes.add(ws_ingresos.cell(row, 2))
                ws_ingresos.cell(row, 1, self.todos_los_meses[numeroDeMes-1])
                if factura.metodoDePago == "PUE" or factura.tipoDeComprobante == "P":
                    ws_ingresos.cell(row, 2, self.todos_los_meses[numeroDeMes-1])
                if factura.UUID in self.complementosDePago:
                    numeroDeMesP = int(self.complementosDePago[factura.UUID]["fechaUltimoPago"].split("-")[1])
                    ws_ingresos.cell(row, 2, self.todos_los_meses[numeroDeMesP-1])
                ws_ingresos.cell(row, 3, factura.UUID)
                ws_ingresos.cell(row, 4, factura.fechaTimbrado)
                ws_ingresos.cell(row, 5, factura.ReceptorRFC)
                ws_ingresos.cell(row, 6, factura.ReceptorNombre)
                ws_ingresos.cell(row, 7, factura.conceptos[0]['descripcion'])
                ws_ingresos.cell(row, 8, factura.subTotal)
                ws_ingresos.cell(row, 9, factura.traslados["IVA"]["importe"])
                ws_ingresos.cell(row, 10, factura.importe)
                ws_ingresos.cell(row, 11, factura.retenciones["ISR"])
                ws_ingresos.cell(row, 12, factura.retenciones["IVA"])
                ws_ingresos.cell(row, 13, factura.total)
                ws_ingresos.cell(row, 14, factura.metodoDePago)

                status = "Pendiente"
                if factura.metodoDePago == "PUE":
                    status = "Pagado"
                if factura.metodoDePago == "PPD":
                    if factura.UUID in self.complementosDePago:
                        if factura.total - self.complementosDePago[factura.UUID]["suma"] < 0.5:
                            status = "Pagado"
                if factura.tipoDeComprobante == "P":
                    status = "Pagado"

                dv.add(ws_ingresos.cell(row, 15))
                ws_ingresos.cell(row, 15, status)

                if factura.UUID in self.complementosDePago:
                    ws_ingresos.cell(row, 16, self.complementosDePago[factura.UUID]["suma"])

                if factura.tipoDeComprobante == "N":
                    ws_ingresos.cell(row, 17, "Nómina")


            ws_ingresos.cell(row+1, 8, "=SUM(H2:H"+str(row)+")")
            ws_ingresos.cell(row+1, 9, "=SUM(I2:I"+str(row)+")")
            ws_ingresos.cell(row+1, 10, "=SUM(J2:J"+str(row)+")")
            ws_ingresos.cell(row+1, 11, "=SUM(K2:K"+str(row)+")")
            ws_ingresos.cell(row+1, 12, "=SUM(L2:L"+str(row)+")")
            ws_ingresos.cell(row+1, 13, "=SUM(M2:M"+str(row)+")")

            ws_ingresos.cell(2, 23, "Facturado")#bajo protesta
            ws_ingresos.cell(3, 20, "Mes")
            ws_ingresos.cell(3, 21, "SUBTOTAL")
            ws_ingresos.cell(3, 22, "I.V.A.")
            ws_ingresos.cell(3, 23, "IMPORTE")
            ws_ingresos.cell(3, 24, "RET ISR")
            ws_ingresos.cell(3, 25, "RET IVA")
            ws_ingresos.cell(3, 26, "T O T A L")

            ws_ingresos.cell(4, 20, "ENERO")
            ws_ingresos.cell(5, 20, "FEBRERO")
            ws_ingresos.cell(6, 20, "MARZO")
            ws_ingresos.cell(7, 20, "ABRIL")
            ws_ingresos.cell(8, 20, "MAYO")
            ws_ingresos.cell(9, 20, "JUNIO")
            ws_ingresos.cell(10, 20, "JULIO")
            ws_ingresos.cell(11, 20, "AGOSTO")
            ws_ingresos.cell(12, 20, "SEPTIEMBRE")
            ws_ingresos.cell(13, 20, "OCTUBRE")
            ws_ingresos.cell(14, 20, "NOVIEMBRE")
            ws_ingresos.cell(15, 20, "DICIEMBRE")

            for renglonMes in range(4,16):
                ws_ingresos.cell(renglonMes, 21, '=SUMIFS(H:H,B:B,T'+str(renglonMes)+',O:O,"Pagado",Q:Q,"<>Nómina")')
                ws_ingresos.cell(renglonMes, 22, '=SUMIFS(I:I,B:B,T'+str(renglonMes)+',O:O,"Pagado",Q:Q,"<>Nómina")')
                ws_ingresos.cell(renglonMes, 23, '=SUMIFS(J:J,B:B,T'+str(renglonMes)+',O:O,"Pagado",Q:Q,"<>Nómina")')
                ws_ingresos.cell(renglonMes, 24, '=SUMIFS(K:K,B:B,T'+str(renglonMes)+',O:O,"Pagado",Q:Q,"<>Nómina")')
                ws_ingresos.cell(renglonMes, 25, '=SUMIFS(L:L,B:B,T'+str(renglonMes)+',O:O,"Pagado",Q:Q,"<>Nómina")')
                ws_ingresos.cell(renglonMes, 26, '=SUMIFS(M:M,B:B,T'+str(renglonMes)+',O:O,"Pagado",Q:Q,"<>Nómina")')

            ws_ingresos.cell(16, 21, "=SUM(U4:U15)")
            ws_ingresos.cell(16, 22, "=SUM(V4:V15)")
            ws_ingresos.cell(16, 23, "=SUM(W4:W15)")
            ws_ingresos.cell(16, 24, "=SUM(X4:X15)")
            ws_ingresos.cell(16, 25, "=SUM(Y4:Y15)")
            ws_ingresos.cell(16, 26, "=SUM(Z4:Z15)")


            ws_ingresos.cell(19, 23, "Nómina")
            ws_ingresos.cell(20, 20, "Mes")
            ws_ingresos.cell(20, 21, "SUBTOTAL")
            ws_ingresos.cell(20, 22, "I.V.A.")
            ws_ingresos.cell(20, 23, "IMPORTE")
            ws_ingresos.cell(20, 24, "RET ISR")
            ws_ingresos.cell(20, 25, "RET IVA")
            ws_ingresos.cell(20, 26, "T O T A L")

            ws_ingresos.cell(21, 20, "ENERO")
            ws_ingresos.cell(22, 20, "FEBRERO")
            ws_ingresos.cell(23, 20, "MARZO")
            ws_ingresos.cell(24, 20, "ABRIL")
            ws_ingresos.cell(25, 20, "MAYO")
            ws_ingresos.cell(26, 20, "JUNIO")
            ws_ingresos.cell(27, 20, "JULIO")
            ws_ingresos.cell(28, 20, "AGOSTO")
            ws_ingresos.cell(29, 20, "SEPTIEMBRE")
            ws_ingresos.cell(30, 20, "OCTUBRE")
            ws_ingresos.cell(31, 20, "NOVIEMBRE")
            ws_ingresos.cell(32, 20, "DICIEMBRE")

            for renglonMes in range(21,33):
                ws_ingresos.cell(renglonMes, 21, '=SUMIFS(H:H,B:B,T'+str(renglonMes)+',O:O,"Pagado",Q:Q,"Nómina")')
                ws_ingresos.cell(renglonMes, 22, '=SUMIFS(I:I,B:B,T'+str(renglonMes)+',O:O,"Pagado",Q:Q,"Nómina")')
                ws_ingresos.cell(renglonMes, 23, '=SUMIFS(J:J,B:B,T'+str(renglonMes)+',O:O,"Pagado",Q:Q,"Nómina")')
                ws_ingresos.cell(renglonMes, 24, '=SUMIFS(K:K,B:B,T'+str(renglonMes)+',O:O,"Pagado",Q:Q,"Nómina")')
                ws_ingresos.cell(renglonMes, 25, '=SUMIFS(L:L,B:B,T'+str(renglonMes)+',O:O,"Pagado",Q:Q,"Nómina")')
                ws_ingresos.cell(renglonMes, 26, '=SUMIFS(M:M,B:B,T'+str(renglonMes)+',O:O,"Pagado",Q:Q,"Nómina")')

            ws_ingresos.cell(33, 21, "=SUM(U21:U32)")
            ws_ingresos.cell(33, 22, "=SUM(V21:V32)")
            ws_ingresos.cell(33, 23, "=SUM(W21:W32)")
            ws_ingresos.cell(33, 24, "=SUM(X21:X32)")
            ws_ingresos.cell(33, 25, "=SUM(Y21:Y32)")
            ws_ingresos.cell(33, 26, "=SUM(Z21:Z32)")

            self.style_ws_ingresos(ws_ingresos,17,row+1)

            workbook.save(self.annual_xlsx_path)

    def hazAgregados(self,paths):
        print(self.complementosDePago)



        workbook = load_workbook(self.annual_xlsx_path)
        if not "Conceptos" in workbook.sheetnames:
            ws_todos = workbook.create_sheet("Conceptos")

        if "iva_por_categria" in workbook.sheetnames:
            sheet1 = workbook["IVA_anual"]
            workbook.remove_sheet(sheet1)
        if "importe_por_categria" in workbook.sheetnames:
            sheet1 = workbook["Importe_anual"]
            workbook.remove_sheet(sheet1)

        ws_cats = workbook.create_sheet("IVA_anual")
        ws_cats_importe = workbook.create_sheet("Importe_anual")
        ws_lista_cats = workbook.create_sheet("Categorias")
        r = 0
        for cat in self.lista_categorias_default:
            r += 1
            ws_lista_cats.cell(r, 1, cat)

        for mes in self.meses:
            ws_mes = workbook[mes]
            for row in range(2,len(ws_mes["A"])):
                if ws_mes.cell(row, 11).value == "PPD":#11 H
                    print("ajustaria"+ ws_mes.cell(row, 3).value)
                    if ws_mes.cell(row, 3).value in self.complementosDePago:
                        ws_mes.cell(row, 15, self.complementosDePago[ws_mes.cell(row, 3).value]["suma"])
                        if ws_mes.cell(row, 9).value - self.complementosDePago[ws_mes.cell(row, 3).value]["suma"] < 0.5:
                            ws_mes.cell(row, 13, "Pagado")

        ws_todos.cell(1, 1, "mes")
        ws_todos.cell(1, 2, 'clave_concepto')
        ws_todos.cell(1, 3, 'UUID')
        ws_todos.cell(1, 4, 'cantidad')
        ws_todos.cell(1, 5, 'descripcion')
        ws_todos.cell(1, 6, 'importeConcepto')
        ws_todos.cell(1, 7, 'descuento')
        ws_todos.cell(1, 8, 'subTotal')
        ws_todos.cell(1, 9, 'impuestos')
        ws_todos.cell(1, 10, 'total')
        ws_todos.cell(1, 11, 'tipo')
        ws_todos.cell(1, 12, 'status')

        row = 1
        # for mes in meses:
        #     if mes in meses_folders:
        #         for concepto in self.conceptos[mes]:

        #dv_categorias = DataValidation(type="list", formula1='"{}"'.format(self.texto_para_validacion), allow_blank=True)
        dv_categorias = DataValidation(type="list", formula1="=Categorias!A1:A"+str(len(self.lista_categorias_default)), allow_blank=True)

        ws_todos.add_data_validation(dv_categorias)
        for concepto in self.conceptos:
            if not self.yaEstaba[concepto['mes']]:
                row += 1
                ws_todos.cell(row, 1, concepto['mes'])
                ws_todos.cell(row, 2, concepto['clave_concepto'])
                ws_todos.cell(row, 3, concepto['UUID'])
                ws_todos.cell(row, 4, concepto['cantidad'])
                ws_todos.cell(row, 5, concepto['descripcion'])
                ws_todos.cell(row, 6, concepto['importeConcepto'])
                ws_todos.cell(row, 7, concepto['descuento'])
                ws_todos.cell(row, 8, concepto['importeConcepto'] - concepto['descuento'])
                ws_todos.cell(row, 9, concepto['impuestos'])
                ws_todos.cell(row, 10, (concepto['importeConcepto'] - concepto['descuento']) + concepto['impuestos'])
                dv_categorias.add(ws_todos.cell(row, 11))
                ws_todos.cell(row, 11, concepto['tipo'])
                ws_todos.cell(row, 12, "=VLOOKUP(C"+str(row)+","+concepto['mes']+"!C:N,11,FALSE)")

        df = pd.DataFrame(self.conceptos)



        self.calculaAgregados(df, ws_cats, 'impuestos')
        self.style_ws(ws_cats, self.columna_totales, self.sumas_row)

        self.calculaAgregados(df, ws_cats_importe, 'importeConcepto')
        self.style_ws(ws_cats_importe, self.columna_totales, self.sumas_row)


        workbook.save(self.annual_xlsx_path)

    def agregaMes(self, mes):
        if os.path.isfile(self.annual_xlsx_path):
            workbook = load_workbook(self.annual_xlsx_path)
            if not mes in workbook.sheetnames:
                self.yaEstaba[mes] = False
                ws_mes = workbook.create_sheet(mes)
            else:
                self.yaEstaba[mes] = True
        else:
            workbook = Workbook()
            ws_mes = workbook.create_sheet(mes)
            sheet1_name = workbook.get_sheet_names()[0]
            sheet1 = workbook[sheet1_name]
            workbook.remove_sheet(sheet1)
            self.yaEstaba[mes] = False


        ws_mes.cell(1, 1, "clave_ps")
        ws_mes.cell(1, 2,     "Fecha")
        ws_mes.cell(1, 3,     "UUID")
        ws_mes.cell(1, 4,     "Nombre")
        ws_mes.cell(1, 5,     "RFC")
        ws_mes.cell(1, 6,     "Concepto")
        ws_mes.cell(1, 7,     "Sub")
        ws_mes.cell(1, 8,     "IVA")
        ws_mes.cell(1, 9,     "Total")
        ws_mes.cell(1, 10,     "F-Pago")
        ws_mes.cell(1, 11,     "M-Pago")
        ws_mes.cell(1, 12,     "Tipo")
        ws_mes.cell(1, 13,     "Status")
        ws_mes.cell(1, 14,     "TipoDeComprobante")
        ws_mes.cell(1, 15,     "complementosDePago")

        dv = DataValidation(type="list", formula1='"Pendiente,Pagado"', allow_blank=True)
        ws_mes.add_data_validation(dv)

        row = 1
        for factura in self.listaDeFacturasOrdenadas:
            row += 1
            ws_mes.cell(row, 1, factura.conceptos[0]['clave_concepto'])
            ws_mes.cell(row, 2, factura.fechaTimbrado)
            ws_mes.cell(row, 3, factura.UUID)
            ws_mes.cell(row, 4, factura.EmisorNombre)
            ws_mes.cell(row, 5, factura.EmisorRFC)
            ws_mes.cell(row, 6, factura.conceptos[0]['descripcion'])
            ws_mes.cell(row, 7, factura.subTotal)
            ws_mes.cell(row, 8, factura.traslados["IVA"]["importe"])
            ws_mes.cell(row, 9, factura.total)
            ws_mes.cell(row, 10, factura.formaDePagoStr)
            ws_mes.cell(row, 11, factura.metodoDePago)
            ws_mes.cell(row, 12, factura.conceptos[0]['tipo'])
            status = "Pendiente"
            if factura.metodoDePago == "PUE":
                status = "Pagado"
            if factura.metodoDePago == "PPD":
                if factura.UUID in self.complementosDePago:
                    if factura.total - self.complementosDePago[factura.UUID]["suma"] < 0.5:
                        status = "Pagado"
            if factura.tipoDeComprobante == "P":
                status = "Pagado"

            dv.add(ws_mes.cell(row, 13))
            ws_mes.cell(row, 13, status)
            ws_mes.cell(row, 14, factura.tipoDeComprobante)
            if factura.UUID in self.complementosDePago:
                ws_mes.cell(row, 15, self.complementosDePago[factura.UUID]["suma"])

            if factura.tipoDeComprobante == "P":
                print("segun "+ factura.UUID + "del mes " +mes+ ", aqui buscaria en todos los meses el uuid "+factura.IdDocumento+" y si encuentra su factura modificaria, la columna 13 del renglon de esa factura en el mes que esté, a Pagado")

        workbook.save(self.annual_xlsx_path)

    def hazResumenDiot(self,currentDir):
        home = os.path.expanduser('~')
        template_folder = os.path.join(home, 'Documents', 'huiini')
        workbook = load_workbook(os.path.join(template_folder,"template_diot.xlsx"))
        ws_rfc = workbook[workbook.get_sheet_names()[0]]
        xlsx_path = os.path.join(currentDir,os.path.join("huiini","resumen.xlsx"))
        #workbook = xlsxwriter.Workbook(xlsx_path)
        #worksheet = workbook.add_worksheet("por_RFC")
        # workbook = Workbook()
        # ws_rfc = workbook.create_sheet("por_RFC")
        # sheet1_name = workbook.get_sheet_names()[0]
        # sheet1 = workbook[sheet1_name]
        # workbook.remove_sheet(sheet1)

        # ws_rfc.cell(1, 1,     "RFC")
        # ws_rfc.cell(1, 2,     "SUBTOTAL")
        # ws_rfc.cell(1, 3,     "DESCUENTO")
        # ws_rfc.cell(1, 4,     "IMPORTE")
        # ws_rfc.cell(1, 5,     "IVA")
        # ws_rfc.cell(1, 6,     "TOTAL")

        row = 5
        for key, value in self.diccionarioPorRFCs.items():
            row += 1
            if row > 9:
                ws_rfc.insert_rows(row)
                for c in range(1,23):
                    cell = ws_rfc.cell(row + 1, c)
                    new_cell = ws_rfc.cell(row, c)
                    new_cell._style = copy(cell._style)
            ws_rfc.cell(row, 3, key)
            ws_rfc.cell(row, 8, value['importeStr'])
            # ws_rfc.cell(row, 2, value['subTotal'])
            # ws_rfc.cell(row, 3, value['descuento'])
            # ws_rfc.cell(row, 4, value['trasladoIVA'])factura.EmisorNombre
            ws_rfc.cell(row, 5, value['nombre'])
            ##factura.EmisorNombre
            ws_rfc.cell(row, 20, value['trasladoIVAStr'])
            # ws_rfc.cell(row, 6, value['total'])
        ws_rfc.cell(row+2, 8, "=SUM(H6:H"+str(row)+")")
        ws_rfc.cell(row+2, 20, "=SUM(T6:T"+str(row)+")")


        #worksheet2 = workbook.add_worksheet("por_Factura")
        ws_factura = workbook.create_sheet("por_Factura")
        ws_factura.cell(1, 1, "clave_ps")
        ws_factura.cell(1, 2,     "Fecha")
        ws_factura.cell(1, 3,     "UUID")
        ws_factura.cell(1, 4,     "Nombre")
        ws_factura.cell(1, 5,     "RFC")
        ws_factura.cell(1, 6,     "Concepto")
        ws_factura.cell(1, 7,     "Sub")
        ws_factura.cell(1, 8,     "IVA")
        ws_factura.cell(1, 9,     "Total")
        ws_factura.cell(1, 10,     "F-Pago")
        ws_factura.cell(1, 11,     "M-Pago")
        ws_factura.cell(1, 12,     "Tipo")

        row = 1
        for factura in self.listaDeFacturasOrdenadas:
            row += 1
            ws_factura.cell(row, 1, factura.conceptos[0]['clave_concepto'])
            ws_factura.cell(row, 2, factura.fechaTimbrado)
            ws_factura.cell(row, 3, factura.UUID)
            ws_factura.cell(row, 4, factura.EmisorNombre)
            ws_factura.cell(row, 5, factura.EmisorRFC)
            ws_factura.cell(row, 6, factura.conceptos[0]['descripcion'])
            ws_factura.cell(row, 7, factura.subTotal)
            ws_factura.cell(row, 8, factura.traslados["IVA"]["importe"])
            ws_factura.cell(row, 9, factura.total)
            ws_factura.cell(row, 10, factura.formaDePagoStr)
            ws_factura.cell(row, 11, factura.metodoDePago)
            ws_factura.cell(row, 12, factura.conceptos[0]['tipo'])

        row += 1
        ws_factura.cell(row, 7,     "=SUM(G2:G"+str(row-1)+")")
        ws_factura.cell(row, 8,     "=SUM(H2:H"+str(row-1)+")")
        ws_factura.cell(row, 9,     "=SUM(I2:I"+str(row-1)+")")

        workbook.save(xlsx_path)








        #url_get = "http://huiini.pythonanywhere.com/resumen"


        # r = requests.get(url_get, stream=True,
        #                 auth=(self.w.username.text(), self.w.password.text()))
        # time_old.sleep(1)
        # if r.status_code == 200:
        #     with open(join(join(self.esteFolder,"huiini"), 'resumenDiot.xlsx'),'wb') as f:
        #         r.raw.decode_content = True
        #         shutil.copyfileobj(r.raw, f)



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


        suSubtotal = float(self.tableWidget_xml.item(row,6).text())
        suDescuento = float(self.tableWidget_xml.item(row,7).text())
        suTrasladoIVA = float(self.tableWidget_xml.item(row,8).text())
        suImporte = float(self.tableWidget_xml.item(row,6).text())-float(self.tableWidget_xml.item(row,7).text())
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
        for columna in range(6,13):
            suma = 0
            for renglon in range(self.numeroDeFacturasValidas):
                try:
                    suma += float(self.tableWidget_xml.item(renglon, columna).text())
                except:
                    print("no puedo")

            self.tableWidget_resumen.setItem(renglonResumen,columna-3,QTableWidgetItem(str(suma)))

        if renglonResumen == 1:
            self.tableWidget_resumen.setItem(0,1,QTableWidgetItem("            ---------"))
            self.tableWidget_resumen.setItem(0,2,QTableWidgetItem("Sumatoria del Periodo Original"))
            self.tableWidget_resumen.setItem(1,1,QTableWidgetItem("Resumen Diot Actualizado"))
            self.tableWidget_resumen.setItem(1,2,QTableWidgetItem("Sumatoria del Periodo Actualizada"))
            self.tableWidget_resumen.setCellWidget(1,0,ImgWidgetPalomita(self))
            self.tableWidget_resumen.setCellWidget(0,0,ImgWidgetTache(self))


    def ponEncabezado(self,lista_columnas):
        n = -1
        for columna in lista_columnas:
            n += 1
            self.tableWidget_xml.setHorizontalHeaderItem (n, QTableWidgetItem(columna))




        # self.tableWidget_xml.setHorizontalHeaderItem (0, QTableWidgetItem("Pdf"))
        # self.tableWidget_xml.setHorizontalHeaderItem (1, QTableWidgetItem("Fecha"))
        # self.tableWidget_xml.setHorizontalHeaderItem (2, QTableWidgetItem("UUID"))
        # self.tableWidget_xml.setHorizontalHeaderItem (3, QTableWidgetItem("Receptor"))
        # self.tableWidget_xml.setHorizontalHeaderItem (4, QTableWidgetItem("Emisor"))
        # self.tableWidget_xml.setHorizontalHeaderItem (5, QTableWidgetItem("Concepto"))
        # self.tableWidget_xml.setHorizontalHeaderItem (7, QTableWidgetItem("Subtotal"))
        # self.tableWidget_xml.setHorizontalHeaderItem (8, QTableWidgetItem("Descuento"))
        # self.tableWidget_xml.setHorizontalHeaderItem (9, QTableWidgetItem("Traslado\nIVA"))
        # self.tableWidget_xml.setHorizontalHeaderItem (10, QTableWidgetItem("Traslado\nIEPS"))
        # self.tableWidget_xml.setHorizontalHeaderItem (11, QTableWidgetItem("Retención\nIVA"))
        # self.tableWidget_xml.setHorizontalHeaderItem (12, QTableWidgetItem("Retención\nISR"))
        # self.tableWidget_xml.setHorizontalHeaderItem (13, QTableWidgetItem("Total"))
        # self.tableWidget_xml.setHorizontalHeaderItem (14, QTableWidgetItem("Forma\nPago"))
        # self.tableWidget_xml.setHorizontalHeaderItem (15, QTableWidgetItem("Método\nPago"))



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

            egresos_folder = self.esteFolder.replace("INGRESOS", "EGRESOS")
            xml =join(egresos_folder + os.sep,self.tableWidget_xml.item(row, 2).text()+".xml")
            #acrobatPath = r'C:/Program Files (x86)/Adobe/Acrobat Reader DC/Reader/AcroRd32.exe'
            #subprocess.Popen("%s %s" % (acrobatPath, pdf))
            try:
                print("este guey me pico:"+xml)
                os.startfile(xml)
            except:
                print ("el sistema no tiene una aplicacion por default para abrir xmls")
                QMessageBox.information(self, "Information", "El sistema no tiene una aplicación por default para abrir xmls" )

        if column == 0:
            egresos_folder = self.esteFolder.replace("INGRESOS", "EGRESOS")
            pdf = join(join(egresos_folder,"huiini"),self.tableWidget_xml.item(row, 2).text()+".pdf")
            #acrobatPath = r'C:/Program Files (x86)/Adobe/Acrobat Reader DC/Reader/AcroRd32.exe'
            #subprocess.Popen("%s %s" % (acrobatPath, pdf))
            try:
                print("este guey me pico:"+pdf)
                os.startfile(pdf)
            except:
                print ("el sistema no tiene una aplicacion por default para abrir pdfs")
                QMessageBox.information(self, "Information", "El sistema no tiene una aplicación por default para abrir pdfs" )


    def meDoblePicaronResumen(self, row,column):
        print("me picaron en : " +str(row)+", " +str(column))
        #excel = join(join(self.esteFolder,"huiini"),"resumen.xlsx")
        #acrobatPath = r'C:/Program Files (x86)/Adobe/Acrobat Reader DC/Reader/AcroRd32.exe'
        #subprocess.Popen("%s %s" % (acrobatPath, pdf))
        try:
            os.startfile(self.excel_path)
            print("este guey me pico:"+self.excel_path)
        except:
            print ("el sistema no tiene una aplicacion por default para abrir exceles")
            QMessageBox.information(self, "Information", "El sistema no tiene una aplicación por default para abrir exceles" )

    def cambiaSeleccionDeImpresora(self, curr, prev):
        print(curr.text())
        self.impresoraDefault = curr.text()
        win32print.SetDefaultPrinter(self.impresoraDefault)

    def cambiaImpresora(self):
        # self.tabWidget.setCurrentIndex(1)
        self.listaDeImpresoras.setEnabled(True)

        for (a,b,name,d) in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL):
            self.listaDeImpresoras.addItem(name)

    def cancelaImpresion(self):
        print("cancelaria")
        phandle = win32print.OpenPrinter(win32print.GetDefaultPrinter())

        print_jobs = win32print.EnumJobs(phandle, 0, -1, 1)
        # jobs = []
        # if print_jobs:
        #     jobs.extend(list(print_jobs))

        for job in print_jobs:

            print(job['TotalPages'])

            if(job['TotalPages'] >= 1):
                print(type(job))
                win32print.SetJob(phandle, job['JobId'], 0, None, win32print.JOB_CONTROL_DELETE)

        win32print.ClosePrinter(phandle)



    def imprime(self):
        #objetosMagicosOrdenados = sorted(self.objetosMagicos, key=lambda objetosMagicos: objetosMagicos.fecha)
        for renglon in range(0,self.tableWidget_xml.rowCount()-1):
            uuid = self.tableWidget_xml.item(renglon,2).text()
            if float(self.tableWidget_xml.item(renglon,12).text()) < 0.000001:
                print("no imprimo facturas con total menores a 0")
            else:
                if self.tableWidget_xml.item(renglon,14).text() == "None":
                    print("no imprimo pagos seño")
                else:
                    printing_folder = self.esteFolder.replace("INGRESOS","EGRESOS")
                    pdf_path = join(join(printing_folder,"huiini"), uuid+".pdf")
                    args = [
                            "-dPrinted", "-dBATCH", "-dNOSAFER", "-dNOPAUSE", "-dNOPROMPT"
                            "-q",
                            "-dNumCopies#1",
                            "-sDEVICE#mswinpr2",
                            f'-sOutputFile#"%printer%{win32print.GetDefaultPrinter()}"',
                            f'"{pdf_path}"'
                        ]

                    encoding = locale.getpreferredencoding()
                    args = [a.encode(encoding) for a in args]
                    ghostscript.Ghostscript(*args)

        for factura in self.listaDeFacturasOrdenadas:

            pdf_path = join(join(self.esteFolder,"huiini"), factura.UUID+".pdf")
            args = [
                    "-dPrinted", "-dBATCH", "-dNOSAFER", "-dNOPAUSE", "-dNOPROMPT"
                    "-q",
                    "-dNumCopies#1",
                    "-sDEVICE#mswinpr2",
                    f'-sOutputFile#"%printer%{win32print.GetDefaultPrinter()}"',
                    f'"{pdf_path}"'
                ]

            encoding = locale.getpreferredencoding()
            args = [a.encode(encoding) for a in args]
            ghostscript.Ghostscript(*args)



        #hh = win32api.ShellExecute(0, "print", join(join(self.esteFolder,"huiini"), "resumenDiot.pdf") , None,  ".",  0)
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
    def borraAuxiliares(self):
        contador = 0
        for t in range(0,10):
            time_old.sleep((1.0*len(self.listaDeFacturasOrdenadas)/10.0))

        contador = 0
        for archivo in os.listdir(self.esteFolder):
            if ".tex" in archivo:
                contador += 1
                eltex = join(self.esteFolder + os.sep,archivo)
                os.remove(eltex)
        for archivo in os.listdir(join(self.esteFolder,"huiini")):
            if ".log" in archivo:
                contador += 1
                ellog = join(join(self.esteFolder,"huiini"),archivo)
                os.remove(ellog)
        for archivo in os.listdir(join(self.esteFolder,"huiini")):
            if ".aux" in archivo:
                contador += 1
                elaux = join(join(self.esteFolder,"huiini"),archivo)
                os.remove(elaux)

        self.progressBar.hide()

    def cualCarpeta(self):
        self.folder.hide()
        file_dialog = getFilesDlg()
        file_dialog.sendPaths.connect(self.procesaCarpetas)
        file_dialog.exec()

    def procesaCarpetas(self,paths):
        self.paths = paths.copy()
        self.progressBar.show()
        self.progressBar.setValue(1)
        folder_cliente = os.path.split(os.path.split(self.paths[0])[0])[0]
        self.json_path = join(folder_cliente, "categorias_huiini.json")
        if os.path.exists(self.json_path):
            with open(self.json_path, "r", encoding="utf-8") as jsonfile:
                lista_de_tuplas = json.load(jsonfile)
        else:
            lista_de_tuplas = []
        self.lista_ordenada = sorted(lista_de_tuplas, key=lambda tup: tup[1])
        self.lista_categorias_default = []
        # self.lista_categorias_default = ["Combustible",
        #                             "Pasajes",
        #                             "Peajes",
        #                             "Consumo en Restaurante",
        #                             "Alimentos",
        #                             "Hospedaje",
        #                             "Teléfono",
        #                             "Internet",
        #                             "Equipo de Computo",
        #                             "Nómina",
        #                             "Institución Bancaria",
        #                             "Gastos Admin",
        #                             "Servcios Admin",
        #                             "Renta",
        #                             "Gasto Personal",
        #                             "Renta de Equipo",
        #                             "Envios",
        #                             "Soporte Técnico",
        #                             "Papeleria",
        #                             "Mant. Auto",
        #                             "Seguros",
        #                             "Mant. Oficina",
        #                             "Estacionamiento",
        #                             "Donativos",
        #                             "Gestion de Eventos",
        #                             "Politicas de Salud",
        #                             "Equipos Multimedia"]

        with open(join(scriptDirectory,"categorias_default.json"), "r", encoding="utf-8") as jf:
            self.lista_categorias_default = json.load(jf)
        for tupla in self.lista_ordenada:
            if not tupla[1] in self.lista_categorias_default:
                self.lista_categorias_default.append(tupla[1])



        #self.texto_para_validacion = ",".join(self.lista_categorias_default)
        #self.texto_para_validacion = ",".join(["oo","uu ú","aa aa"])
        self.texto_para_validacion = "oo,u uú"
        print(self.texto_para_validacion)
        self.todos_los_meses = ["ENERO","FEBRERO","MARZO","ABRIL","MAYO","JUNIO","JULIO","AGOSTO","SEPTIEMBRE","OCTUBRE","NOVIEMBRE","DICIEMBRE"]

        self.conceptos = []
        self.yaEstaba = {}
        self.complementosDePago = {}
        self.meses = []
        print(paths[0])
        year_folder = os.path.split(paths[0])[0]
        same_year = True
        no_son_meses = False

        huiini_home_folder = os.path.split(os.path.split(year_folder)[0])[0]
        print(huiini_home_folder)

        home = os.path.expanduser('~')
        pdflatex_folder_path = os.path.join(home, 'Documents', 'huiini')
        with open(os.path.join(pdflatex_folder_path,"huiini_home_folder_path.txt"), "w") as f:
            f.write(huiini_home_folder)
        for path in paths:
            mes = os.path.split(path)[1]
            mes = ''.join([i for i in mes if not i.isdigit()])
            mes = mes.strip()
            if not mes in self.todos_los_meses:
                no_son_meses = True
            if year_folder != os.path.split(path)[0]:
                same_year = False

        if not same_year or no_son_meses:
            if no_son_meses:
                QMessageBox.information(self, "Información", "no son meses")
            else:
                QMessageBox.information(self, "Información", "no son el mismo año")
        else:
            print(year_folder)
            year = os.path.split(os.path.split(paths[0])[0])[1]
            client = os.path.split(os.path.split(os.path.split(paths[0])[0])[0])[1]
            print(client+"_"+year)

            reply = QMessageBox.question(self, 'Message',"Crear pdfs?", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.hacerPDFs = True
            else:
                self.hacerPDFs = False

            self.annual_xlsx_path = os.path.join(year_folder, client+"_"+year + ".xlsx")
            if os.path.isfile(self.annual_xlsx_path):#borra el anterior
                os.remove(self.annual_xlsx_path)

            if len(self.paths) > 1:
                self.excel_path = self.annual_xlsx_path
            else:
                self.excel_path = join(self.paths[0],"EGRESOS","huiini","resumen.xlsx")

            self.listaDeFacturasIngresos = []

            p = 0
            for path in paths:
                p += 1
                progreso = int(100*(p/(len(paths)+2)))
                self.procesaEgresos(path)
                self.pon_categorias_custom_por_factura(paths)
                self.agregaMes(self.mes)
                self.procesaIngresos(path)
                self.aislaNomina(path)
                self.progressBar.setValue(progreso)


            self.hazTabDeIngresos(paths)
            p += 1
            progreso = int(100*(p/(len(paths)+2)))
            self.progressBar.setValue(progreso)
            self.pon_categorias_custom_por_concepto(paths)
            self.hazAgregados(paths)
            p += 1
            progreso = int(100*(p/(len(paths)+2)))
            self.progressBar.setValue(progreso)
            self.agrega_cats.setEnabled(True)
            self.raise_()
            self.activateWindow()
            self.progressBar.hide()

    def pon_categorias_custom_por_factura(self,paths):

        folder_cliente = os.path.split(os.path.split(paths[0])[0])[0]
        json_path = join(folder_cliente,"categorias_huiini.json")
        hay_categorias_custom = False
        if os.path.exists(json_path):
            hay_categorias_custom = True
            with open(json_path, "r") as jsonfile:
                self.lista_de_empiezos = json.load(jsonfile)


        if hay_categorias_custom:
            for factura in self.listaDeFacturasOrdenadas:
                for concepto in factura.conceptos:
                    clave = concepto["clave_concepto"]

                    for empiezo in self.lista_de_empiezos:
                        if clave.startswith(empiezo[0]):
                            concepto["tipo"] = empiezo[1]


    def pon_categorias_custom_por_concepto(self,paths):
        folder_cliente = os.path.split(os.path.split(paths[0])[0])[0]
        json_path = join(folder_cliente,"categorias_huiini.json")
        hay_categorias_custom = False
        if os.path.exists(json_path):
            hay_categorias_custom = True
            with open(json_path, "r") as jsonfile:
                self.lista_de_empiezos = json.load(jsonfile)


        if hay_categorias_custom:
            for concepto in self.conceptos:
                clave = concepto["clave_concepto"]
                for empiezo in self.lista_de_empiezos:
                    if clave.startswith(empiezo[0]):
                        concepto["tipo"] = empiezo[1]

    def procesaIngresos(self, path):
        self.esteFolder = join(path,"INGRESOS")
        if os.path.isdir(self.esteFolder):
            if not os.path.exists(join(self.esteFolder, "huiini")):
                os.makedirs(join(self.esteFolder, "huiini"))
            self.mes = os.path.split(path)[1]
            self.mes = ''.join([i for i in self.mes if not i.isdigit()])
            self.mes = self.mes.strip()
            cuantosDuplicados = 0
            self.listaDeDuplicados = []
            self.listaDeFacturas = []
            self.listaDeUUIDs = []
            contador = 0
            for archivo in os.listdir(self.esteFolder):
                if archivo.endswith(".xml"):
                    laFactura = Factura(join(self.esteFolder + os.sep,archivo))
                    if laFactura.sello == "SinSello":
                        print("Omitiendo xml sin sello "+laFactura.xml_path)
                    else:
                        if laFactura.version:
                            if laFactura.UUID in self.listaDeUUIDs:

                                cuantosDuplicados+=1
                                self.listaDeDuplicados.append(laFactura.UUID)
                            else:
                                self.listaDeUUIDs.append(laFactura.UUID)
                                contador += 1
                                self.listaDeFacturas.append(laFactura)

            self.listaDeFacturasOrdenadas = sorted(self.listaDeFacturas, key=lambda listaDeFacturas: listaDeFacturas.fechaTimbrado)
            if cuantosDuplicados > 0:
                mensaje = "En ingresos hay "+str(cuantosDuplicados)+" duplicados\n"
                chunks = []
                for esteDuplicado in self.listaDeDuplicados:
                    chunks.append(str(esteDuplicado)+"\n")
                mensaje2 = "".join(chunks)
                mensaje = mensaje + mensaje2
                QMessageBox.information(self, "Information", mensaje)

            # for t in range(0,5):
            #     time_old.sleep(0.05*len(self.listaDeFacturasOrdenadas))
            #     self.pd.setValue(self.pd.value() + ( (100 - self.pd.value()) / 2))
            contador = 0

            los_facturas = self.listaDeFacturasOrdenadas.copy()
            self.listaDeFacturasIngresos.extend(los_facturas)
            for factura in self.listaDeFacturasOrdenadas:
                #self.pd.setValue(50*((contador + 1)/len(self.listaDeFacturasOrdenadas)))
                factura.setFolio(contador + 1)
                if factura.tipoDeComprobante == "P":
                    if factura.IdDocumento in self.complementosDePago:
                        self.complementosDePago[factura.IdDocumento]["suma"] += factura.ImpPagado
                    else:
                        self.complementosDePago[factura.IdDocumento] = {}
                        self.complementosDePago[factura.IdDocumento]["suma"] = factura.ImpPagado

                    self.complementosDePago[factura.IdDocumento]["fechaUltimoPago"] = factura.fechaTimbrado

            if self.hacerPDFs:
                self.hazPDFs()
                time_old.sleep(0.2*len(self.listaDeFacturasOrdenadas))
                self.borraAuxiliares()

    def aislaNomina(self, path):
        esteFolder = join(path,"EGRESOS")

        for archivo in os.listdir(esteFolder):
            if archivo.endswith(".xml"):
                laFactura = Factura(join(esteFolder + os.sep,archivo))
                if laFactura.tipoDeComprobante == "N":
                    if not os.path.exists(join(esteFolder, "Nomina")):
                        os.makedirs(join(esteFolder, "Nomina"))
                    try:
                        os.rename(join(esteFolder + os.sep,archivo), join(esteFolder, "Nomina",archivo))

                    except:
                        print("no pude mover una nómina")


    def procesaEgresos(self, path):
        self.folder.setText("Procesando: " + u'\n' + path)
        self.folder.show()
        self.esteFolder = join(path,"EGRESOS")

        self.mes = os.path.split(path)[1]
        self.mes = ''.join([i for i in self.mes if not i.isdigit()])
        self.mes = self.mes.strip()
        self.meses.append(self.mes) # aqui si self.mes no se puede formar correctamantre deberia dar un error y ventanita que lo explique
        #self.conceptos[self.mes] = []
        if not os.path.exists(join(self.esteFolder, "huiini")):
            os.makedirs(join(self.esteFolder, "huiini"))
        self.tableWidget_xml.clear()
        self.tableWidget_resumen.clear()
        self.tableWidget_resumen.repaint()
        lc = ["Pdf","Fecha","UUID","Receptor","Emisor","Concepto","Subtotal","Descuento","Traslado\nIVA","Traslado\nIEPS","Retención\nIVA","Retención\nISR","Total","Forma\nPago","Método\nPago"]
        self.ponEncabezado(lc)
        self.tableWidget_xml.setRowCount(13)
        self.tableWidget_xml.repaint()
        cuantosDuplicados = 0
        self.listaDeDuplicados= []
        self.listaDeFacturas = []
        self.listaDeUUIDs = []
        contador = 0
        for archivo in os.listdir(self.esteFolder):
            if archivo.endswith(".xml"):

                laFactura = Factura(join(self.esteFolder + os.sep,archivo))
                if laFactura.sello == "SinSello":
                    print("Omitiendo xml sin sello "+laFactura.xml_path)
                else:
                    if laFactura.version:
                        if laFactura.UUID in self.listaDeUUIDs:

                            cuantosDuplicados+=1
                            self.listaDeDuplicados.append(laFactura.UUID)
                        else:
                            self.listaDeUUIDs.append(laFactura.UUID)
                            contador += 1
                            self.listaDeFacturas.append(laFactura)
        if os.path.exists(join(self.esteFolder, "Nomina")):
            for archivo in os.listdir(join(self.esteFolder, "Nomina")):
                if archivo.endswith(".xml"):

                    laFactura = Factura(join(join(self.esteFolder, "Nomina") + os.sep,archivo))
                    if laFactura.sello == "SinSello":
                        print("Omitiendo xml sin sello "+laFactura.xml_path)
                    else:
                        if laFactura.version:
                            if laFactura.UUID in self.listaDeUUIDs:

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



        if cuantosDuplicados > 0:
            mensaje = "En egresos hay "+str(cuantosDuplicados)+" duplicados\n"
            chunks = []
            for esteDuplicado in self.listaDeDuplicados:
                chunks.append(str(esteDuplicado)+"\n")
            mensaje2 = "".join(chunks)
            mensaje = mensaje + mensaje2
            QMessageBox.information(self, "Information", mensaje)

        contador = 0
        for factura in self.listaDeFacturasOrdenadas:
            factura.setFolio(contador + 1)
            los_conceptos = factura.conceptos.copy()
            for concepto in los_conceptos:
                concepto["mes"] = self.mes
                concepto["UUID"] = factura.UUID
                if concepto["impuestos"]:
                    concepto["impuestos"] = float(concepto['impuestos'])
                else:
                    concepto["impuestos"] = 0
            self.conceptos.extend(los_conceptos)

            if factura.tipoDeComprobante == "P":
                if factura.IdDocumento in self.complementosDePago:
                    self.complementosDePago[factura.IdDocumento]["suma"] += factura.ImpPagado
                else:
                    self.complementosDePago[factura.IdDocumento] = {}
                    self.complementosDePago[factura.IdDocumento]["suma"] = factura.ImpPagado

                self.complementosDePago[factura.IdDocumento]["fechaUltimoPago"] = factura.fechaTimbrado

            if factura.tipoDeComprobante == "N":
                self.listaDeFacturasIngresos.append(factura)


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
            self.tableWidget_xml.setItem(contador,6,self.esteItem(str(factura.subTotal),""))
            self.tableWidget_xml.setItem(contador,7,self.esteItem(str(factura.descuento),""))
            self.tableWidget_xml.setItem(contador,8,self.esteItem(str(factura.traslados["IVA"]["importe"]),""))
            self.tableWidget_xml.setItem(contador,9,self.esteItem(str(factura.traslados["IEPS"]["importe"]),""))
            self.tableWidget_xml.setItem(contador,10,self.esteItem(str(factura.retenciones["IVA"]),""))
            self.tableWidget_xml.setItem(contador,11,self.esteItem(str(factura.retenciones["ISR"]),""))
            self.tableWidget_xml.setItem(contador,12,self.esteItem(str(factura.total),""))
            self.tableWidget_xml.setItem(contador,13,self.esteItem(factura.formaDePagoStr,""))
            self.tableWidget_xml.setItem(contador,14, self.esteItem(factura.metodoDePago,factura.metodoDePago))

            pdf_dir = os.path.join(os.path.dirname(factura.tex_path),"huiini")
            pdf_name = os.path.split(factura.tex_path)[1].replace("tex","pdf")
            pdf_path = os.path.join(pdf_dir,pdf_name)
            if os.path.exists(pdf_path):
                self.tableWidget_xml.setCellWidget(contador,0, ImgWidgetPalomita(self))

            if factura.EmisorRFC in self.diccionarioPorRFCs:
                self.diccionarioPorRFCs[factura.EmisorRFC]['subTotal'] += float(factura.subTotal)
                self.diccionarioPorRFCs[factura.EmisorRFC]['descuento'] += float(factura.descuento)
                self.diccionarioPorRFCs[factura.EmisorRFC]['trasladoIVA'] += float(factura.traslados['IVA']['importe'])
                self.diccionarioPorRFCs[factura.EmisorRFC]['importe'] += float(factura.subTotal)-float(factura.descuento)
                self.diccionarioPorRFCs[factura.EmisorRFC]['total'] += float(factura.total)
                self.diccionarioPorRFCs[factura.EmisorRFC]['importeStr'] += "+"+str(float(factura.subTotal)-float(factura.descuento))
                self.diccionarioPorRFCs[factura.EmisorRFC]['trasladoIVAStr'] += "+"+str(factura.traslados['IVA']['importe'])
                print("sumale " + str(factura.subTotal) )
            else:
                self.diccionarioPorRFCs[factura.EmisorRFC] = {'subTotal': float(factura.subTotal),
                                                              'descuento': float(factura.descuento),
                                                              'trasladoIVA': float(factura.traslados['IVA']['importe']),
                                                              'importe': float(factura.subTotal)-float(factura.descuento),
                                                              'total': float(factura.total),
                                                              'importeStr': "="+str(float(factura.subTotal)-float(factura.descuento)),
                                                              'trasladoIVAStr': "="+str(factura.traslados['IVA']['importe']),
                                                              'nombre': factura.EmisorNombre
                                                            }
                print("crealo con " + str(factura.subTotal))

            contador +=1




        # for t in range(0,5):
        #     time_old.sleep(0.05*len(self.listaDeFacturasOrdenadas))
        #     self.pd.setValue(self.pd.value() + ( (100 - self.pd.value()) / 2))



        if self.hacerPDFs:
            self.hazPDFs()
            time_old.sleep(0.2*len(self.listaDeFacturasOrdenadas))
            self.borraAuxiliares()


        contador = -1

        # time_old.sleep(0.5*len(self.listaDeFacturasOrdenadas))

        self.imprimir.setEnabled(True)

        self.numeroDeFacturasValidas = len(self.listaDeFacturasOrdenadas)


        self.sumale()

        self.hazResumenDiot(self.esteFolder)
        #if len(paths)>2:

        self.tableWidget_resumen.setItem(0,1,QTableWidgetItem("Resumen Diot"))
        self.tableWidget_resumen.setItem(0,2,QTableWidgetItem("Sumatoria del Periodo"))
        self.tableWidget_resumen.setCellWidget(0,0, ImgWidgetPalomita(self))

        #obtener los warnings de las facturas
        mensajeAlerta =""
        for factura in self.listaDeFacturasOrdenadas:
            if not factura.mensaje == "":
                mensajeAlerta += factura.UUID + factura.mensaje + r'\n'
        if not mensajeAlerta == "":
            QMessageBox.information(self, "Information", mensajeAlerta)




        self.folder.setText("Carpeta Procesada: " + u'\n' + self.esteFolder)
        self.folder.show()

app = QtWidgets.QApplication(sys.argv)
app.setStyleSheet("QMessageBox { messagebox-text-interaction-flags: 5; }")
form = Ui_MainWindow()
form.show()


app.exec_()
