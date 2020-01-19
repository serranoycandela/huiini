#-*- encoding: utf-8 -*-
from jinja2 import Template
import xml.etree.ElementTree as etree  
import os
import jinja2
from subprocess import Popen
import codecs
import sys
from contextlib import contextmanager



class Factura:
    
    def __init__(self, xml_path):
        self.midir = os.path.dirname(os.path.realpath(__file__))
        #self.pdflatex_path = os.path.join(self.midir + os.sep,"C:/Program Files/MiKTeX 2.9/miktex/bin/x64/pdflatex.exe")
        #self.pdflatex_path = "C:/Users/SICAD/Dropbox/Generador de PDF/TestWxPython/miktex/bin/pdflatex.exe"
        
        self.pdflatex_path = "pdflatex"
        print(self.pdflatex_path)
        self.xml_path = xml_path
        
        xml_dir = os.path.dirname(self.xml_path)
        self.xml_name = os.path.basename(self.xml_path)
        
        pdfs_dir = os.path.join(xml_dir + os.sep,"pdfs")
#        if not os.path.exists(pdfs_dir):
#            os.makedirs(pdfs_dir)
            
        self.mensaje = ""
        #self.dictForma
        
        self.folio = 1
        
        tree = etree.parse(xml_path)
    
        self.root = tree.getroot()
        
        self.getTags()
        
        self.version = self.root.get ("Version")
        if self.version == None: 
            self.version = self.root.get ("version")
        if self.version == "3.2":
            
            
            self.folioKey = "folio"
            self.serieKey = "serie"
            self.formaDePagoKey = "formaDePago"
            self.LugarExpedicionKey = "LugarExpedicion"
            self.metodoDePagoKey = "metodoDePago"
            self.subTotalKey = "subTotal"
            self.descuentoKey = "descuento"
            self.selloKey = "sello"
            self.noCertificadoKey = "noCertificado"
            self.certificadoKey = "certificado"   
            self.totalKey = "total"   
            self.tipoDeComprobanteKey = "tipoDeComprobante" 
            self.EmisorRFCKey = "rfc" 
            self.EmisorNombreKey = "nombre"   
            
            self.receptorRfcKey = "rfc"
            self.receptorNombreKey = "nombre"
            
            self.conceptoDescripcionKey = "descripcion"   
            self.conceptoImporteKey = "importe"
            self.conceptoValorUnitarioKey = "valorUnitario"
            self.conceptoUnidadKey = "unidad"
            self.conceptoCantidadKey = "cantidad"
            
            self.retImpuestoKey = "impuesto"
            #self.retTasaKey = "tasa"
            self.retImporteKey = "importe"
            
            self.trasImpuestoKey = "impuesto"
            self.trasTasaKey = "tasa"
            self.trasImporteKey = "importe"
            
            self.selloCFDKey = "selloCFD"
            self.selloSATKey = "selloSAT"
            self.noCertificadoSATKey = "noCertificadoSAT"
            
            self.ImpLocTrasladadoKey = "ImpLocTrasladado"
            self.TasadeTrasladoKey = "TasadeTraslado"
            
            self.totalImpuestosTrasladadosKey = "totalImpuestosTrasladados"
            
            RegimenFiscalTag = self.EmisorTag.find("{http://www.sat.gob.mx/cfd/3}RegimenFiscal")
            self.EmisorRegimen = self.latexStr(RegimenFiscalTag.get("Regimen")) 
            
            
        if self.version == "3.3":
            self.folioKey = "Folio"
            self.serieKey = "Serie"
            self.formaDePagoKey = "FormaPago"
            self.LugarExpedicionKey = "LugarExpedicion"
            self.metodoDePagoKey = "MetodoPago"
            self.subTotalKey = "SubTotal"
            self.descuentoKey = "Descuento"
            self.selloKey = "Sello"
            self.noCertificadoKey = "NoCertificado"
            self.certificadoKey = "Certificado"
            self.totalKey = "Total"  
            self.tipoDeComprobanteKey = "TipoDeComprobante"     
            self.EmisorRFCKey = "Rfc"
            self.EmisorNombreKey = "Nombre"
            self.receptorRfcKey = "Rfc"
            self.receptorNombreKey = "Nombre"
            
            self.trasImpuestoKey = "Impuesto"
            self.trasTasaKey = "TasaOCuota"
            self.trasImporteKey = "Importe"
            
            self.retImpuestoKey = "Impuesto"
            self.retTasaKey = "TasaOCuota"
            self.retImporteKey = "Importe"
            
            self.conceptoDescripcionKey = "Descripcion"   
            self.conceptoImporteKey = "Importe"
            self.conceptoValorUnitarioKey = "Valorunitario"
            self.conceptoUnidadKey = "Unidad"
            self.conceptoCantidadKey = "Cantidad"
            
            self.selloCFDKey = "SelloCFD"
            self.selloSATKey = "SelloSAT"
            self.noCertificadoSATKey = "NoCertificadoSAT"
            
            self.ImpLocTrasladadoKey = "TotalTrasladado" ############################################## ???????????????????????????????????????????????
            self.TasadeTrasladoKey = "TasaTraslado"         ######################################################## ???????????????????????????????????????????
            
            self.totalImpuestosTrasladadosKey = "totalImpuestosTrasladados" #############################????????????????
            self.EmisorRegimen = self.latexStr(self.EmisorTag.get("RegimenFiscal")) 
             
        
        if self.version:
            self.cosas_comunes_32_33()
            self.sumale()
            self.setMetodo()
          
            
    def setMetodo(self):
        dictMetodo = {"01":"Efectivo",
                       "02":"Cheque nominativo",
                       "03":"Transferencia Electrónica de Fondos",
                       "04":"Tarjeta de Crédito",
                       "05":"Monedero Electrónico",
                       "06":"Dinero Electrónico",
                       "08":"Vales de Despensa",
                       "28":"Tarjeta de Débito",
                       "29": "Tarjeta de Servicio",
                       "99":"Otros"}  
        if self.metodoDePago in dictMetodo:
            self.metodoDePagoStr = dictMetodo[self.metodoDePago] 
        else: 
            self.metodoDePagoStr = self.metodoDePago
            
    def latexStr(self, strCorrupto):
        
        if strCorrupto:
            strBien = strCorrupto.replace("»?", "Ó")
            strBien = strBien.replace("Ã³", "ó")
            strBien = strBien.replace("«?", "ó")
            strBien = strBien.replace("½?", "ó")
            strBien = strBien.replace("#", "")
            strBien = strBien.replace("N°", "No.")
            strBien = strBien.replace("Ã?â?°", "É")
            strBien = strBien.replace("#", "")
            strBien = strBien.replace("¾", " ")
            strBien = strBien.replace("_", " ")
            strBien = strBien.replace("&", " Y ")
            strBien = strBien.replace("#", "N") 
            strBien = strBien.replace("▄", "Ñ")  
            strBien = strBien.replace("#", "")
            strBien = strBien.replace("$", "")
            strBien = strBien.replace("´", "")
            strBien = strBien.replace("_", " ")
            strBien = strBien.replace("&", " ")
            strBien = strBien.replace("-", " ")
            strBien = strBien.replace("°", " ")
            strBien = strBien.replace("¹", " ")
            strBien = strBien.replace("%", " ")
            strBien = strBien.replace("^", " ")
            strBien = strBien.replace("�", " ")
            strBien = strBien.replace("┬Ö", " ")
            strBien = strBien.replace(u'\x99', " ")
            strBien = strBien.replace(u'\x7f', "Ñ")
            
            
        else:
            strBien = "None"
        return strBien
                        
            
    def setFolio(self,folio):
        self.miFolio = folio
        
            
        
           
            
    def sumale(self):
        
        #self.sumaDeRetenciones = self.retenciones.IVA + self.retenciones.ISR ####sera?????????
        self.sumaDeRetenciones = sum(self.retenciones.values())
        
        self.sumaDeTraslados = 0.0
        for traslado in self.traslados.values(): 
            self.sumaDeTraslados += traslado["importe"]
        
        self.sumaDeTrasladosLocales = 0.0
        for traslado in self.trasladosLocales.values(): 
            self.sumaDeTrasladosLocales += traslado["importe"]
            
       
        self.sumaDeRetencionesLocales = 0.0
        for retencion in self.retencionesLocales.values(): 
            self.sumaDeRetencionesLocales += retencion["importe"]
        
        
        self.sumaDeImportes = 0.0
        for concepto in self.conceptos:
            self.sumaDeImportes += concepto["importeConcepto"]
            
        self.elementosDeLaTabla = []
        
        if self.sumaDeImportes > 0.0:
            self.elementosDeLaTabla.append({"cosa": "Suma de importes", "tasa": "--", "importe": self.sumaDeImportes})
            
        if self.descuento > 0.0:
            self.elementosDeLaTabla.append({"cosa": "Descuento", "tasa": "--", "importe": self.descuento})
        
        for impuesto, importe in self.retenciones.items():
            if importe > 0.0:
                self.elementosDeLaTabla.append({"cosa": "Retencion "+ impuesto, "tasa": "--", "importe": importe})
        
        for impuesto, valor in self.traslados.items():
            if valor["importe"] > 0.0:
                self.elementosDeLaTabla.append({"cosa": "Traslado "+ impuesto, "tasa": "--", "importe": valor["importe"]})
                
        
            
        for impuesto, valor in self.retencionesLocales.items():
            if valor["importe"] > 0.0:
                self.elementosDeLaTabla.append({"cosa": "Retencion (complemento) "+ impuesto, "tasa": "--", "importe": valor["importe"]})
        
        for impuesto, valor in self.trasladosLocales.items():
            if valor["importe"] > 0.0:
                self.elementosDeLaTabla.append({"cosa": "Traslado (complemento) "+ impuesto, "tasa": "--", "importe": valor["importe"]})    
        if self.subTotal > 0.0:
            self.elementosDeLaTabla.append({"cosa": "Subtotal ", "tasa": "--", "importe": self.subTotal})    
        if self.sumaDeRetenciones > 0.0:
            self.elementosDeLaTabla.append({"cosa": "Suma de retenciones", "tasa": "--", "importe": self.sumaDeRetenciones})
        if self.sumaDeTraslados > 0.0:
            self.elementosDeLaTabla.append({"cosa": "Suma de traslados", "tasa": "--", "importe": self.sumaDeTraslados})
        if self.sumaDeTrasladosLocales > 0.0:
            self.elementosDeLaTabla.append({"cosa": "Suma de traslados(complemento)", "tasa": "--", "importe": self.sumaDeTrasladosLocales})
        if self.sumaDeRetencionesLocales > 0.0:
            self.elementosDeLaTabla.append({"cosa": "Suma de retenciones(complemento)", "tasa": "--", "importe": self.sumaDeRetencionesLocales})
        if self.total > 0.0:
            self.elementosDeLaTabla.append({"cosa": "Total ", "tasa": "--", "importe": self.total})
        
        
        
        #if self.totalDeImpuestosTrasladados > 0.0:
        #    self.elementosDeLaTabla.append({"cosa": "Total de Impuestos Trasladados ", "tasa": "--", "importe": self.totalDeImpuestosTrasladados})
        
        
        
    
    def conviertemeEnTex(self):
        ## aqui va lo del template
        def getTemplate(tpl_path):
            path, filename = os.path.split(tpl_path)
            return jinja2.Environment(
                loader=jinja2.FileSystemLoader(path or './')
            ).get_template(filename)
        
        self.tex_path = os.path.dirname(self.xml_path)+ "/"+self.UUID+".tex"
        print(self.tex_path) 
        context = {
            'miFolio' : self.miFolio,
            'folio': self.folio,
            'serie': self.serie,
            'nombre_receptor': self.ReceptorNombre,
            'rfc_emisor': self.EmisorRFC,
            'descuento': self.descuento,
            'tipoDeComprobante': self.tipoDeComprobante,
            'regimen_emisor': self.EmisorRegimen,
            'LugarExpedicion': self.LugarExpedicion,
            'rfc_receptor': self.ReceptorRFC,
            'nombre_emisor': self.EmisorNombre,
            'UUID': self.UUID,
            'formaDePago': self.formaDePago,
            'metodoDePago': self.metodoDePago,
            'fechaTimbrado': self.fechaTimbrado,
            'noCertificadoSAT': self.noCertificadoSAT,
            'selloCFD': self.selloCFD,
            'selloSAT': self.selloSAT,
            'conceptos': self.conceptos,
#             'retencionIVA': self.retenciones["IVA"],
#             'rencionISR': self.retenciones["ISR"],
#             'trasladoIVA': self.traslados["IVA"],
#             'subTotal': self.subTotal,
#             'retencionIVA': 0,
#             'retencionISR': 0,
#             'totalDeImpuestosTrasladados': self.totalImpuestosTrasladados,
#             'sumaDeRetenciones': self.sumaDeRetenciones,
#             'sumaDeTraslados': self.sumaDeTraslados,
#             'sumaDeTrasladosLocales': self.sumaDeTrasladosLocales,
#             'sumaDeRetencionesLocales': self.sumaDeRetencionesLocales,
#             'sumaDeImportes': self.sumaDeImportes,
#             'Total': self.total,
            'elementosDeLaTabla': self.elementosDeLaTabla
            
            
            
        }
        template = getTemplate("template2.jinja")
        with codecs.open (self.tex_path, "w", "utf-8") as miFile:
            output = template.render(context)
        
            # jinja returns unicode - so `output` needs to be encoded to a bytestring
            # before writing it to a file
            miFile.write(output)
        
        
        
        #getTemplate("template.jinja").stream(context).dump(self.tex_path)
        
       
    def conviertemeEnPDF(self,currentDir): 
        
        try:
        
            if os.path.exists(os.path.join(self.midir + os.sep, os.path.basename(self.tex_path)[:-3]+"pdf")):
                os.remove(os.path.join(self.midir + os.sep, os.path.basename(self.tex_path)[:-3]+"pdf"))
                
            try:
                from subprocess import DEVNULL # Python 3
            except ImportError:
                DEVNULL = open(os.devnull, 'r+b', 0)
            
#             Popen(["-output-directory", currentDir,self.tex_path], stdin=DEVNULL, stdout=DEVNULL, stderr=DEVNULL)
            print(self.pdflatex_path, str(self.tex_path))
            
            Popen([self.pdflatex_path, "-output-directory", currentDir,self.tex_path]) 
            #Popen([self.pdflatex_path, str(self.tex_path)]) 
        #"-output-directory=" +  self.midir,
            return 1
        except:
            print("aqui valio madre")
            return 0
        
        
    def getTags (self):
        self.EmisorTag = self.root.find("{http://www.sat.gob.mx/cfd/3}Emisor")
        self.ReceptorTag = self.root.find("{http://www.sat.gob.mx/cfd/3}Receptor")
        self.conceptos = []
        self.conceptosTag = self.root.find("{http://www.sat.gob.mx/cfd/3}Conceptos") 
        self.impuestosTag = self.root.find("{http://www.sat.gob.mx/cfd/3}Impuestos") 
        self.ComplementoTag = self.root.find("{http://www.sat.gob.mx/cfd/3}Complemento") 
        
    def arreglaSusPendejadas(self, impuesto):
        ################################################################# nadie le creyó al macfly, se confirmo
        if impuesto == "001":
            return "ISR"
        elif impuesto == "002":
            return "IVA"
        elif impuesto == "003":
            return "ISH" ############################################################### ojo
        elif impuesto == "004":
            return "TUA"
        elif impuesto == "005":
            return "IEPS"
        else:
            return impuesto    
        
    def cosas_comunes_32_33(self):
         
        print("version " + self.version)
        
        self.folio = self.latexStr(self.root.get (self.folioKey))
        self.serie = self.latexStr(self.root.get(self.serieKey))
        self.formaDePago = self.latexStr(self.root.get(self.formaDePagoKey))
        
        
        self.LugarExpedicion = self.latexStr(self.root.get(self.LugarExpedicionKey))
        
        self.subTotal = float(self.root.get(self.subTotalKey))
        
        self.descuento = self.latexStr(self.root.get(self.descuentoKey))
        try:
            self.descuento = float(self.descuento)
        except:
            self.descuento = 0     
        
        self.sello = self.root.get (self.selloKey)[:50] + "..."
        
        
        
        self.metodoDePago = self.latexStr(self.root.get (self.metodoDePagoKey))
       
        
        self.noCertificado = self.latexStr(self.root.get (self.noCertificadoKey))
        
        self.certificado = self.root.get (self.certificadoKey)[:50] + "..."
        self.total = float(self.root.get(self.totalKey))
        
        self.tipoDeComprobante = self.latexStr(self.root.get (self.tipoDeComprobanteKey))
        
        
        self.EmisorRFC = self.latexStr(self.EmisorTag.get(self.EmisorRFCKey))
        self.EmisorNombre = self.latexStr(self.EmisorTag.get(self.EmisorNombreKey))
        if not self.EmisorNombre:
            self.EmisorNombre = "NONAME"                         
        
        self.ReceptorRFC = self.latexStr(self.ReceptorTag.get(self.receptorRfcKey)) 
        self.ReceptorNombre = self.latexStr(self.ReceptorTag.get(self.receptorNombreKey))
                 
        ############################################################  CONCEPTOS TAG ############################################################################    
        if self.conceptosTag == None:
            print("no hay traslados")
        else:
            listaconceptosTag = self.conceptosTag.findall ("{http://www.sat.gob.mx/cfd/3}Concepto")
            for conceptoTag in listaconceptosTag:
                if conceptoTag == None:
                    print("no hay traslados")
                else: 
                    #print(conceptoTag)
                    if conceptoTag == None:
                        print("no tiene impuestos transladados")
                    else:
                        descripcion = self.latexStr(conceptoTag.get(self.conceptoDescripcionKey))

                        importeConcepto = float(conceptoTag.get(self.conceptoImporteKey))
                        
                        valorUnitario = self.latexStr(conceptoTag.get(self.conceptoValorUnitarioKey))
                        
                        unidad = self.latexStr(conceptoTag.get(self.conceptoUnidadKey))
                        
                        cantidad = self.latexStr(conceptoTag.get(self.conceptoCantidadKey))
                        
                        self.conceptos.append({"cantidad":cantidad, "unidad":unidad, "valorUnitario":valorUnitario, "importeConcepto":importeConcepto, "descripcion":descripcion})
        
        self.retenciones = {"IVA":0,"ISR":0,"IEPS":0,"ISH":0,"TUA":0}
        
        
        #################################################    IMPEUSTOS TAG  ##################################################################################
        if self.impuestosTag == None:
            print("no hay impuestos")
            retImporte = "0"
            retImpuestoString = "Retencion" 
        else:
            self.totalImpuestosTrasladados = self.latexStr(self.impuestosTag.get(self.totalImpuestosTrasladadosKey))
            
            
            retencionesTag = self.impuestosTag.find ("{http://www.sat.gob.mx/cfd/3}Retenciones") 
            if retencionesTag == None:
                retImporte = "0"
                retImpuestoString = "Retencion de IVA" 
                retImpuestoString = "Retencion de ISR" 
            else:
                listaRetencionTag = retencionesTag.findall ("{http://www.sat.gob.mx/cfd/3}Retencion")
                
                
                for retencionTag in listaRetencionTag:
                    try:
                        if retencionTag == None:
                            print("no hay retenciones")
                            retImpuesto = "0"
                            retImporte = "nada"
                        else: 
                            retImpuesto = self.latexStr(retencionTag.get (self.retImpuestoKey))
                            retImporte = self.latexStr(retencionTag.get (self.retImporteKey))
                            
                                
                            self.retenciones[self.arreglaSusPendejadas(retImpuesto)] = float(retImporte)  
                    except:
                        self.mensaje += " no pudo agregar retencion"   
                        
            
               
        self.traslados = {"IVA":{"importe":0,"tasa":0},"ISR":{"importe":0,"tasa":0},"IEPS":{"importe":0,"tasa":0},"ISH":{"importe":0,"tasa":0},"TUA":{"importe":0,"tasa":0}}        
        try:
            trasladosTag = self.impuestosTag.find("{http://www.sat.gob.mx/cfd/3}Traslados")
        except:
            trasladosTag = None
            print("no hay traslados en " + self.xml_name )
        if trasladosTag == None:
            print("no hay traslados")
            tasa = "--"
            importe = "0"
            trasImpuestoString = "Traslado" 
        else:
            listatrasladosTag = trasladosTag.findall ("{http://www.sat.gob.mx/cfd/3}Traslado")

                       
            for trasladoTag in listatrasladosTag:
                if trasladoTag == None:
                    print("no hay traslados")
                else: 
                    if trasladoTag == None:
                        print("no tiene impuestos transladados")
                    else:
                        try:
                            impuesto = self.latexStr(trasladoTag.get(self.trasImpuestoKey))
                            tasa = self.latexStr(trasladoTag.get(self.trasTasaKey))
                            importe = self.latexStr(trasladoTag.get(self.trasImporteKey))
                        
                            #self.traslados[self.arreglaSusPendejadas(impuesto)] = {"importe":importe,"tasa":tasa}
                            #self.traslados[self.arreglaSusPendejadas(impuesto)].importe += float(importe)
                            
                            print("impuesto "+impuesto)
                            print("impuesto "+ self.arreglaSusPendejadas(impuesto))
                            print("importe " + str(self.traslados[self.arreglaSusPendejadas(impuesto)]["importe"]))
                            
                            try:
                                if self.traslados[self.arreglaSusPendejadas(impuesto)]["importe"] == 0:
                                    self.traslados[self.arreglaSusPendejadas(impuesto)]["tasa"] = "NA"
                                else:
                                    self.traslados[self.arreglaSusPendejadas(impuesto)]["tasa"] = tasa
                                
                                self.traslados[self.arreglaSusPendejadas(impuesto)]["importe"] += float(importe)
                            except:
                                print("no pude sumar en " + self.UUID)
                                self.mensaje += " no pudo sumar un traslado"
                        except:
                            print("no pude sumar en " + self.UUID)
                            self.mensaje += " no pudo sumar un traslado"
                        
                        
        #######################################################  COMPLEMENTO TAG   ########################################################                
        if self.ComplementoTag == None:
            print("no hay comp")
        else:
            self.trasladosLocales = {"IVA":{"importe":0,"tasa":0},"ISR":{"importe":0,"tasa":0},"IEPS":{"importe":0,"tasa":0},"ISH":{"importe":0,"tasa":0},"TUA":{"importe":0,"tasa":0}}
            TimbreFiscalDigitalTag = self.ComplementoTag.find("{http://www.sat.gob.mx/TimbreFiscalDigital}TimbreFiscalDigital")
            self.UUID = TimbreFiscalDigitalTag.get ("UUID")
            self.selloCFD = TimbreFiscalDigitalTag.get (self.selloCFDKey)[:50] + "..."
            self.selloSAT = TimbreFiscalDigitalTag.get (self.selloSATKey)[:50] + "..."
            self.noCertificadoSAT = TimbreFiscalDigitalTag.get (self.noCertificadoSATKey)
            self.fechaTimbrado = TimbreFiscalDigitalTag.get ("FechaTimbrado")
            self.retencionesLocales = {"IVA":{"importe":0,"tasa":0},"ISR":{"importe":0,"tasa":0},"IEPS":{"importe":0,"tasa":0},"ISH":{"importe":0,"tasa":0},"TUA":{"importe":0,"tasa":0}}   
            ImpuestosLocalesTag = self.ComplementoTag.find("{http://www.sat.gob.mx/implocal}ImpuestosLocales")
            if ImpuestosLocalesTag : 
            
                
                listaDeTrasladosLocalesTag = ImpuestosLocalesTag.findall("{http://www.sat.gob.mx/implocal}TrasladosLocales")# findall
                #self.sumaDeTrasladosLocales = 0
                for trasladosLocalesTag in listaDeTrasladosLocalesTag:
                    if trasladosLocalesTag == None:
                        print("no hay traslados")
                    else:                        
                        try:
                            impuestoLocal = self.latexStr(trasladosLocalesTag.get(self.ImpLocTrasladadoKey))###############################falta la version 3.3
                            tasaLocal = self.latexStr(trasladosLocalesTag.get(self.TasadeTrasladoKey))
                            importeLocal = self.latexStr(trasladosLocalesTag.get("Importe"))
                            
    #                         if self.trasladosLocales[self.arreglaSusPendejadas(impuestoLocal)]["importe"] == 0:
    #                             self.trasladosLocales[self.arreglaSusPendejadas(impuestoLocal)]["tasa"] = "NA"
    #                         else:
    #                             self.trasladosLocales[self.arreglaSusPendejadas(impuestoLocal)]["tasa"] = tasaLocal
                            try:
                                self.trasladosLocales[self.arreglaSusPendejadas(impuestoLocal)]["tasa"] = tasaLocal 
                                self.trasladosLocales[self.arreglaSusPendejadas(impuestoLocal)]["importe"] += float(importeLocal)
                            except: 
                                print("no pude sumar " + self.UUID)
                                self.mensaje += " no pudo sumar un traslado local" 
                        except:
                            print("no pude sumar " + self.UUID)
                            self.mensaje += " no pudo sumar un traslado local"
                    
                        #self.sumaDeTrasladosLocales += float(importeLocal)   
                    
                #self.trasladosLocales[self.arreglaSusPendejadas(impuestoLocal)] = {"importe":importeLocal,"tasa":tasaLocal}
                            
                
              
                listadeRetencionesLocalesTags = ImpuestosLocalesTag.findall("{http://www.sat.gob.mx/implocal}RetencionesLocales") 
                
                for retencionesLocalesTag in listadeRetencionesLocalesTags:
                    try:
                        if retencionesLocalesTag == None:
                            print("no hay traslados")
                        else:  
                            retencionLocal = retencionesLocalesTag.get("ImpLocRetenido")###############################falta la version 3.3
                            tasaRetencionLocal = retencionesLocalesTag.get("TasadeRetencion")
                            importeRetencionLocal = float(retencionesLocalesTag.get("Importe"))
                            self.retencionesLocales[self.arreglaSusPendejadas(retencionLocal)] = {"importe":importeRetencionLocal,"tasa":tasaRetencionLocal}    
        
                    except:
                        self.mensaje += "no pudo agregar retencion local"       
                        
            AerolineasTag = self.ComplementoTag.find("{http://www.sat.gob.mx/aerolineas}Aerolineas")  
            if AerolineasTag :  
                self.trasladosLocales["TUA"] = {"importe": float(AerolineasTag.get("TUA")), "tasa": "--"}         
#         
#    
#         
# 
# f1 = Factura(r'C:\Users\Usuario\workspacePy\TestWxPython\28126587-158F-430D-9536-758EDC63CDF2.xml')
# f2 = Factura(r'C:\Users\Usuario\workspacePy\TestWxPython\589e70c6-1b86-476d-89b3-e7ab216f6a7c.xml')
# 
# print(f1.UUID)
# print(f1.version)
# print(f1.EmisorNombre)
# print(f1.EmisorRFC)
# suma = 0
# for concepto in f1.conceptos:
#     print(concepto["descripcion"])
#     suma += float(concepto["importeConcepto"])
#     
# print("suma : " + str(suma))
# 
# 
# # print("retencion IVA: "+str(f1.retenciones["IVA"]))
# # print("retencion ISR: "+str(f1.retenciones["ISR"]))
# # print("retencion ISH: "+str(f1.retenciones["ISH"]))
# # print("retencion IEPS: "+str(f1.retenciones["IEPS"]))
# # print("retencion TUA: "+str(f1.retenciones["TUA"]))
# 
# print("traslado IVA: importe = "+str(f1.traslados["IVA"]["importe"])+" tasa = "+str(f1.traslados["IVA"]["tasa"]))
# print("traslado ISR: importe = "+str(f1.traslados["ISR"]["importe"])+" tasa = "+str(f1.traslados["ISR"]["tasa"]))
# print("traslado ISH: importe = "+str(f1.traslados["ISH"]["importe"])+" tasa = "+str(f1.traslados["ISH"]["tasa"]))
# print("traslado IEPS: importe = "+str(f1.traslados["IEPS"]["importe"])+" tasa = "+str(f1.traslados["IEPS"]["tasa"]))
# print("traslado TUA: importe = "+str(f1.traslados["TUA"]["importe"])+" tasa = "+str(f1.traslados["TUA"]["tasa"]))
# 
# print("traslado local IVA: importe = "+str(f1.trasladosLocales["IVA"]["importe"])+" tasa = "+str(f1.trasladosLocales["IVA"]["tasa"]))
# print("traslado local ISR: importe = "+str(f1.trasladosLocales["ISR"]["importe"])+" tasa = "+str(f1.trasladosLocales["ISR"]["tasa"]))
# print("traslado local ISH: importe = "+str(f1.trasladosLocales["ISH"]["importe"])+" tasa = "+str(f1.trasladosLocales["ISH"]["tasa"]))
# print("traslado local IEPS: importe = "+str(f1.trasladosLocales["IEPS"]["importe"])+" tasa = "+str(f1.trasladosLocales["IEPS"]["tasa"]))
# print("traslado local TUA: importe = "+str(f1.trasladosLocales["TUA"]["importe"])+" tasa = "+str(f1.trasladosLocales["TUA"]["tasa"]))
# 
#     
# print(f1.conceptos)
# 
# 
# print("--------------------")
# 
# print(f2.UUID)
# print(f2.version)
# print(f2.EmisorNombre)
# print(f2.EmisorRFC)






    
    
# for dir:
#     estaFactura = factura(esteFile)
#     
#     #useTemplate tal que es el template de tex
#     
#     context = {uuid = estaFactura.UUID, nombre = estaFactura.nombreEmisor}
#     
#     render('testTemplate.tex', context)