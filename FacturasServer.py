#-*- encoding: utf-8 -*-
from jinja2 import Template
import xml.etree.ElementTree as etree
import os
import jinja2
from subprocess import Popen
import codecs
import sys
from contextlib import contextmanager
import FacturasClient
import subprocess
#from sh import pdflatex


class FacturaServer(FacturasClient.FacturaClient):

    def __init__(self, xml_path):
        super().__init__(xml_path)

    def conviertemeEnTex(self):
        ## aqui va lo del template
        def getTemplate(tpl_path):
            path, filename = os.path.split(tpl_path)
            return jinja2.Environment(
                loader=jinja2.FileSystemLoader(path or './')
            ).get_template(filename)

        self.tex_path = os.path.dirname(self.xml_path)+ "/"+self.UUID+".tex"

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
        script_path = os.path.dirname(os.path.abspath( __file__ ))
        template = getTemplate(os.path.join(script_path,"template2.jinja"))
        with codecs.open (self.tex_path, "w", "utf-8") as miFile:
            output = template.render(context)

            # jinja returns unicode - so `output` needs to be encoded to a bytestring
            # before writing it to a file
            miFile.write(output)



        #getTemplate("template.jinja").stream(context).dump(self.tex_path)


    def conviertemeEnPDF(self):

        ## aqui falta manejar los posibes errores al generar el pdf

        pdflatex_path = "C:\\Program Files\\MiKTeX 2.9\\miktex\\bin\\x64\\pdflatex.exe"

        subprocess.run([pdflatex_path, self.tex_path],shell=True)


        # os.chdir(os.path.dirname(self.tex_path))
        # conversion = pdflatex(self.tex_path)
        #
        # return conversion.exit_code

	    # s = codecs.open(self.tex_path, "r", "utf-8").read()
        # pdf = None
        # info = None


        # pdf, info = texcaller.convert(s, 'LaTeX', 'PDF', 5)
       	# print(info)


        # if pdf == None:
        #     print("aqui hay que guardar el xml para ver porque no pudo "+self.xml_path)
        #     return(0)
        # else:

        #     pdf_path = self.tex_path[:-3]+"pdf"

        #     f = open(pdf_path,"wb")

        #     f.write(bytes(pdf , "utf-8", "surrogateescape"))

        #     f.close()
        #     return(1)








#        try:
#
#            if os.path.exists(os.path.join(self.midir + os.sep, os.path.basename(self.tex_path)[:-3]+"pdf")):
#                os.remove(os.path.join(self.midir + os.sep, os.path.basename(self.tex_path)[:-3]+"pdf"))
#
#            try:
#                from subprocess import DEVNULL # Python 3
#            except ImportError:
#                DEVNULL = open(os.devnull, 'r+b', 0)
#
##             Popen(["-output-directory", currentDir,self.tex_path], stdin=DEVNULL, stdout=DEVNULL, stderr=DEVNULL)
#            print(self.pdflatex_path, str(self.tex_path))
#
#            Popen([self.pdflatex_path, "-output-directory", currentDir,self.tex_path])
#            #Popen([self.pdflatex_path, str(self.tex_path)])
#        #"-output-directory=" +  self.midir,
#            return 1
#        except:
#            print("aqui valio madre")
#            return 0
#
